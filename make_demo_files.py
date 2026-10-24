#!/usr/bin/env python3
"""
make_demo_files.py - generate sample evidence files for demonstrating DEICMS.

Creates demo_files/ containing:
  * four legitimate evidence files of different categories, one carrying EXIF
    metadata so the extraction step has something to show
  * one file whose content does not match its extension, for demonstrating
    the magic-byte rejection (FR-14)
  * one extra file reserved for a case created live during the oral exam

Run:  python make_demo_files.py
"""
import datetime
import pathlib
import random

OUT = pathlib.Path(__file__).parent / "demo_files"
OUT.mkdir(exist_ok=True)


def crime_scene_photo():
    """A real JPEG carrying EXIF - exercises the Pillow metadata extractor."""
    from PIL import Image
    import piexif
    img = Image.new("RGB", (900, 600), (238, 238, 238))
    px = img.load()
    for x in range(900):                      # simple gradient + marker grid
        for y in range(600):
            px[x, y] = (200 - x // 10, 200 - y // 8, 210)
    for gx in range(0, 900, 100):
        for gy in range(600):
            px[gx, gy] = (40, 40, 40)
    path = OUT / "crime_scene_photo.jpg"
    exif = {
        "0th": {
            piexif.ImageIFD.Make: b"Canon",
            piexif.ImageIFD.Model: b"Canon EOS 5D Mark IV",
            piexif.ImageIFD.Software: b"DEICMS evidence capture",
            piexif.ImageIFD.DateTime: b"2026:03:14 09:41:22",
            piexif.ImageIFD.Artist: b"Forensic Unit 3",
        },
        "Exif": {
            piexif.ExifIFD.DateTimeOriginal: b"2026:03:14 09:41:22",
            piexif.ExifIFD.LensMake: b"Canon",
        },
        "GPS": {
            piexif.GPSIFD.GPSLatitudeRef: b"N",
            piexif.GPSIFD.GPSLatitude: ((38, 1), (11, 1), (1500, 100)),
            piexif.GPSIFD.GPSLongitudeRef: b"E",
            piexif.GPSIFD.GPSLongitude: ((15, 1), (33, 1), (2700, 100)),
        },
        "1st": {}, "thumbnail": None,
    }
    img.save(path, "JPEG", quality=92, exif=piexif.dump(exif))
    return path


def server_access_log():
    path = OUT / "server_access.log"
    base = datetime.datetime(2026, 3, 14, 8, 0, 0)
    ips = ["10.4.17.22", "10.4.17.98", "192.168.2.40", "172.16.8.3"]
    paths = ["/login", "/dashboard", "/cases/7", "/evidence/21/verify",
             "/admin/users", "/assistant/chat", "/cases/7/export"]
    lines = []
    for i in range(420):
        t = base + datetime.timedelta(seconds=i * 37)
        code = random.choice([200, 200, 200, 302, 403, 404, 500])
        lines.append('%s - - [%s] "GET %s HTTP/1.1" %d %d' % (
            random.choice(ips), t.strftime("%d/%b/%Y:%H:%M:%S +0100"),
            random.choice(paths), code, random.randint(180, 9000)))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def transaction_records():
    path = OUT / "transaction_records.csv"
    rows = ["timestamp,account_from,account_to,amount_eur,reference"]
    base = datetime.datetime(2026, 2, 2, 10, 0, 0)
    for i in range(160):
        t = base + datetime.timedelta(minutes=i * 53)
        rows.append("%s,IT%02d0300203280000%06d,IT%02d0300203280000%06d,%.2f,TRX-%05d" % (
            t.isoformat(sep=" "), random.randint(10, 99), random.randint(1, 999999),
            random.randint(10, 99), random.randint(1, 999999),
            random.uniform(25, 18000), 10000 + i))
    path.write_text("\n".join(rows) + "\n", encoding="utf-8")
    return path


def incident_report_pdf():
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    path = OUT / "incident_report.pdf"
    doc = SimpleDocTemplate(str(path), pagesize=A4, title="Incident Report")
    s = getSampleStyleSheet()
    body = [
        Paragraph("Incident Report - Case CASE-2026-004", s["Title"]),
        Spacer(1, 14),
        Paragraph("Reporting officer: Forensic Unit 3", s["Normal"]),
        Paragraph("Date of report: 14 March 2026", s["Normal"]),
        Spacer(1, 14),
        Paragraph("Summary", s["Heading2"]),
        Paragraph(
            "At 09:41 on 14 March 2026 a workstation was seized from the premises "
            "under warrant. The device was powered on at the time of seizure and was "
            "isolated from the network before imaging. A photograph of the scene, the "
            "server access log covering the preceding 72 hours, and an extract of the "
            "associated transaction records were collected as separate exhibits.",
            s["BodyText"]),
        Spacer(1, 10),
        Paragraph("Chain of custody", s["Heading2"]),
        Paragraph(
            "All four exhibits were registered on intake, fingerprinted with SHA-256, "
            "and assigned to the analyst on duty. No transfer took place before "
            "registration.", s["BodyText"]),
    ]
    doc.build(body)
    return path


def spoofed_executable():
    """
    A Windows PE executable given a .png extension.

    The declared extension says image/png; the magic bytes say
    application/x-dosexec, which is in DANGEROUS_MIME_TYPES. The upload must
    therefore be refused - this is the file for the FR-14 screenshot.
    """
    path = OUT / "suspect_photo.png"
    pe = bytearray(b"MZ\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00\xff\xff\x00\x00")
    pe += b"\xb8" + b"\x00" * 0x30
    pe += b"\x80\x00\x00\x00"
    pe += (b"This program cannot be run in DOS mode.\r\r\n$" + b"\x00" * 7)
    pe += b"\x00" * (0x80 - len(pe))
    pe += b"PE\x00\x00\x4c\x01\x03\x00"          # PE signature + COFF header
    pe += b"\x00" * 240
    path.write_bytes(bytes(pe))
    return path


def exam_usb_listing():
    """Reserved for the case created live during the oral exam."""
    path = OUT / "usb_device_listing.txt"
    lines = [
        "USB MASS STORAGE - DIRECTORY LISTING",
        "Device  : Kingston DataTraveler 3.0",
        "Serial  : 60A44C3F8E21B9D0",
        "Captured: 2026-10-24 11:05:00",
        "Imaged  : write-blocker ref WB-114",
        "",
        "Mode    Size (bytes)  Modified             Name",
        "-----   ------------  -------------------  ----------------------------",
    ]
    names = ["ledger_q3.xlsx", "contacts.vcf", "notes.txt", "scan_0012.jpg",
             "backup_2026_09.zip", "readme.md", "invoice_8871.pdf"]
    base = datetime.datetime(2026, 9, 2, 14, 12, 0)
    for i, n in enumerate(names):
        t = base + datetime.timedelta(hours=i * 7)
        lines.append("-a---   %12d  %s  %s" % (
            random.randint(2048, 4_500_000), t.strftime("%Y-%m-%d %H:%M:%S"), n))
    lines += ["", "Total: %d files" % len(names),
              "SHA-256 of device image recorded separately on the intake form."]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


if __name__ == "__main__":
    random.seed(20260314)          # reproducible output
    made = [crime_scene_photo(), server_access_log(), transaction_records(),
            incident_report_pdf(), spoofed_executable(), exam_usb_listing()]
    print("Wrote %d files to %s\n" % (len(made), OUT))
    for p in made:
        print("  %-28s %9d bytes" % (p.name, p.stat().st_size))
