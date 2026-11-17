"""SBAccess reproduction for 3i: ReadAllImagePlanes with ReadOneScoop=0 desynchronises the socket.

Uses only 3i's SBAccess.py (next to this file or importable) and numpy. Read-only:
nothing is written to SlideBook. Pick a small multi-plane capture (e.g. a 65^3 PSF).

    python sbaccess_block_read_repro.py --capture 2 [--timepoint 0] [--channel 0] [--port 65432] [--timing]

What it shows
  1. Reference: every Z plane read with ReadImagePlaneBuf.
  2. ReadAllImagePlanes(..., ReadOneScoop=1): identical to the reference; socket stays in sync.
  3. ReadAllImagePlanes(..., ReadOneScoop=0): the returned stack is shifted by a few bytes
     (SlideBook sends extra bytes before the pixels that SBAccess does not consume), the
     last bytes stay on the socket, and the next command fails with
     "First character in answer must be a: &".
  4. Same read on a fresh connection, then the socket is drained: the leftover is exactly the
     shift, and the next command works again.
  5. (--timing) speed of plane reads vs the block-read variants on this capture, and
     SlideBook's private memory during each (needs psutil).
"""

from __future__ import annotations

import argparse
import socket
import sys
import time

import numpy as np

try:
    from SBAccess import SBAccess
except ImportError:  # Synergy Conductor layout
    from slidebook6.SBAccess import SBAccess


def connect(host: str, port: int):
    sock = socket.create_connection((host, port))
    sock.settimeout(120)
    return sock, SBAccess(sock)


def drain(sock: socket.socket, quiet_s: float = 1.0) -> bytes:
    """Bytes still waiting on the socket (none expected after a complete reply)."""
    old = sock.gettimeout()
    sock.settimeout(quiet_s)
    data = b""
    try:
        while True:
            chunk = sock.recv(1 << 20)
            if not chunk:
                break
            data += chunk
    except (socket.timeout, TimeoutError, OSError):
        pass
    sock.settimeout(old)
    return data


def read_planes(sb, cap, t, ch, nz, ny, nx) -> np.ndarray:
    out = np.empty((nz, ny, nx), dtype=np.uint16)
    for z in range(nz):
        out[z] = np.asarray(sb.ReadImagePlaneBuf(cap, 0, t, z, ch), dtype=np.uint16).reshape(ny, nx)
    return out


def block_read(sb, cap, t, ch, nz, ny, nx, one_scoop: bool) -> np.ndarray:
    arr = np.zeros(nz * ny * nx, dtype=np.uint16)
    sb.ReadAllImagePlanes(cap, t, ch, bool(one_scoop), arr)
    return arr.reshape(nz, ny, nx)


def byte_shift(got: np.ndarray, ref: np.ndarray, max_shift: int = 4096) -> int | None:
    """k such that got's bytes == ref's bytes delayed by k (got[k:] == ref[:-k]); 0 = identical."""
    g, r = got.view(np.uint8).ravel(), ref.view(np.uint8).ravel()
    if np.array_equal(g, r):
        return 0
    for k in range(1, max_shift):
        if np.array_equal(g[k:k + 4096], r[:4096]) and np.array_equal(g[k:], r[:-k]):
            return k
    return None


def sb_private_gb() -> str:
    try:
        import psutil

        procs = [p for p in psutil.process_iter(["name"]) if p.info["name"] and "slidebook" in p.info["name"].lower()]
        return ", ".join(f"{p.memory_info().private / 1e9:.1f} GB" for p in procs) or "n/a"
    except Exception:
        return "n/a (pip install psutil)"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=65432)
    ap.add_argument("--capture", type=int, required=True, help="capture index on the current slide")
    ap.add_argument("--timepoint", type=int, default=0, help="ImageIndex (timepoint) to read")
    ap.add_argument("--channel", type=int, default=0)
    ap.add_argument("--timing", action="store_true", help="also time plane vs block reads")
    a = ap.parse_args()

    sock, sb = connect(a.host, a.port)
    cap, t, ch = a.capture, a.timepoint, a.channel
    slide_id = sb.GetCurrentSlideId()

    nz = int(sb.GetNumZPlanes(cap))
    ny = int(sb.GetNumYRows(cap))
    nx = int(sb.GetNumXColumns(cap))
    print(f"Capture {cap} '{sb.GetImageName(cap)}': {nx} x {ny} x {nz} planes, uint16 "
          f"({nz * ny * nx * 2 / 1e6:.1f} MB); timepoint {t}, channel {ch}")
    if nz < 2:
        print("Choose a capture with more than one Z plane.")
        return 2

    print("\n1. Reference: ReadImagePlaneBuf for every plane")
    ref = read_planes(sb, cap, t, ch, nz, ny, nx)
    print(f"   done; mean {ref.mean():.2f}")

    print("\n2. ReadAllImagePlanes(ReadOneScoop=1)")
    got = block_read(sb, cap, t, ch, nz, ny, nx, True)
    print(f"   identical to reference: {np.array_equal(got, ref)}")
    left = drain(sock)
    print(f"   bytes left on socket: {len(left)}; next command GetNumCaptures -> {sb.GetNumCaptures()}")

    print("\n3. ReadAllImagePlanes(ReadOneScoop=0), then a normal command")
    got = block_read(sb, cap, t, ch, nz, ny, nx, False)
    k = byte_shift(got, ref)
    head = got.view(np.uint8).ravel()[:16]
    print(f"   identical to reference: {np.array_equal(got, ref)}")
    print(f"   data shifted by {k} byte(s); first 16 bytes received: {head.tobytes().hex(' ')}"
          + (f" (as int32: {np.frombuffer(head[:12].tobytes(), '<i4').tolist()})" if k else ""))
    try:
        n = sb.GetNumCaptures()
        print(f"   next command GetNumCaptures -> {n} (no failure on this run)")
    except Exception as exc:
        print(f"   next command GetNumCaptures FAILED: {type(exc).__name__}: {exc}")
    sock.close()

    print("\n4. Fresh connection: ReadAllImagePlanes(ReadOneScoop=0), drain the socket, then a normal command")
    sock, sb = connect(a.host, a.port)
    slide_id = sb.GetCurrentSlideId()
    got = block_read(sb, cap, t, ch, nz, ny, nx, False)
    left = drain(sock)
    tail = ref.view(np.uint8).ravel()[-len(left):].tobytes() if left else b""
    print(f"   bytes left on socket: {len(left)}; they equal the last {len(left)} bytes of the stack: {left == tail}")
    print(f"   next command GetNumCaptures -> {sb.GetNumCaptures()} (in sync again after draining)")

    if a.timing:
        print("\n5. Timing on this capture (fresh reads; small captures may be cached by SlideBook/Windows)")
        for label, fn in (
            ("ReadImagePlaneBuf x nz", lambda: read_planes(sb, cap, t, ch, nz, ny, nx)),
            ("ReadAllImagePlanes one scoop=1", lambda: block_read(sb, cap, t, ch, nz, ny, nx, True)),
        ):
            t0 = time.monotonic()
            fn()
            dt = time.monotonic() - t0
            print(f"   {label:32s} {nz * ny * nx * 2 / 1e9 / dt:6.2f} GB/s   SlideBook private memory {sb_private_gb()}")
        if hasattr(sb, "ReadAllImagePlanesSM") and hasattr(sb, "AllocateSharedMemory"):
            for scoop in (False, True):
                shm = sb.AllocateSharedMemory(nx, ny, nz)
                try:
                    t0 = time.monotonic()
                    arr = sb.ReadAllImagePlanesSM(cap, t, ch, shm, scoop)
                    dt = time.monotonic() - t0
                    same = np.array_equal(arr, ref)
                    del arr
                finally:
                    shm.close()
                    shm.unlink()
                print(f"   {'ReadAllImagePlanesSM scoop=' + str(int(scoop)):32s} {nz * ny * nx * 2 / 1e9 / dt:6.2f} GB/s"
                      f"   identical {same}")
    sock.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
