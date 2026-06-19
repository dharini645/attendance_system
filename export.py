"""
export.py

Exports attendance records from SQLite to a CSV file.
Can export today's records only, or all records ever.

HOW TO USE (standalone):
  python export.py               → exports today's records
  python export.py --all         → exports all records

Or import and call from attendance.py or app.py:
  from export import export_to_csv
  export_to_csv()
"""

import sys
import pandas as pd
from datetime import date
from database import get_all_records, get_today_records


def export_to_csv(all_records: bool = False) -> str:
    """
    Exports attendance data to a CSV file.

    Parameters:
        all_records (bool): If True, exports the full history.
                            If False (default), exports only today.

    Returns:
        str: The path of the CSV file that was created.
    """
    if all_records:
        data     = get_all_records()           # list of dicts with Name, Date, Time
        filename = "attendance_all.csv"
    else:
        raw      = get_today_records()         # list of (name, time) tuples
        today    = str(date.today())
        data     = [{"Name": name, "Date": today, "Time": time} for name, time in raw]
        filename = f"attendance_{today}.csv"

    if not data:
        print("⚠️  No attendance records found to export.")
        return filename

    df = pd.DataFrame(data)

    # Sort by date and then by time for clean ordering
    if "Date" in df.columns:
        df = df.sort_values(by=["Date", "Time"], ascending=[False, True])

    df.to_csv(filename, index=False)
    print(f"✅ Exported {len(df)} record(s) to {filename}")
    return filename


if __name__ == "__main__":
    export_all = "--all" in sys.argv
    export_to_csv(all_records=export_all)