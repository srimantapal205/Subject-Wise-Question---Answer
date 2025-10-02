# **SQL Server Date & Time Handling**:

---

## 1. **Date & Time Data Types**

| Data Type        | Storage   | Format                          | Range                        | Precision                |                 |
| ---------------- | --------- | ------------------------------- | ---------------------------- | ------------------------ | --------------- |
| `DATE`           | 3 bytes   | `YYYY-MM-DD`                    | 0001-01-01 to 9999-12-31     | Day                      |                 |
| `DATETIME`       | 8 bytes   | `YYYY-MM-DD hh:mm:ss[.mmm]`     | 1753-01-01 to 9999-12-31     | 1/300 sec                |                 |
| `SMALLDATETIME`  | 4 bytes   | `YYYY-MM-DD hh:mm:ss`           | 1900-01-01 to 2079-06-06     | Minute                   |                 |
| `DATETIME2`      | 6–8 bytes | `YYYY-MM-DD hh:mm:ss[.nnnnnnn]` | 0001-01-01 to 9999-12-31     | 100 ns                   |                 |
| `DATETIMEOFFSET` | 10 bytes  | `YYYY-MM-DD hh:mm:ss [+         | -hh:mm]`                     | 0001-01-01 to 9999-12-31 | Time zone aware |
| `TIME`           | 3–5 bytes | `hh:mm:ss[.nnnnnnn]`            | 00:00:00 to 23:59:59.9999999 | 100 ns                   |                 |

---

## 2. **Getting Current Date & Time**

```sql
-- Current system datetime (SQL Server local time)
SELECT GETDATE();               -- e.g., 2025-10-02 14:23:55.123

-- UTC datetime
SELECT GETUTCDATE();            -- e.g., 2025-10-02 09:23:55.123

-- Higher precision
SELECT SYSDATETIME();           -- DATETIME2 with fractions
SELECT SYSUTCDATETIME();        -- DATETIME2 UTC
SELECT SYSDATETIMEOFFSET();     -- With offset
```

---

## 3. **Extracting Parts of Date**

```sql
DECLARE @dt DATETIME = '2025-10-02 14:23:55.987';

SELECT 
    YEAR(@dt)     AS YearPart,
    MONTH(@dt)    AS MonthPart,
    DAY(@dt)      AS DayPart,
    DATENAME(WEEKDAY, @dt) AS DayName,
    DATEPART(HOUR, @dt) AS HourPart,
    DATEPART(MINUTE, @dt) AS MinutePart,
    DATEPART(SECOND, @dt) AS SecondPart;
```

---

## 4. **Date Arithmetic**

```sql
DECLARE @dt DATETIME = '2025-10-02 14:23:55';

-- Add/Subtract
SELECT DATEADD(DAY, 10, @dt) AS Add10Days;     -- 2025-10-12
SELECT DATEADD(MONTH, -2, @dt) AS Sub2Months;  -- 2025-08-02

-- Difference
SELECT DATEDIFF(DAY, '2025-01-01', '2025-10-02') AS DaysDiff; -- 274
SELECT DATEDIFF(HOUR, '2025-10-02 08:00', '2025-10-02 14:00') AS HoursDiff; -- 6
```

---

## 5. **Date Formatting**

```sql
DECLARE @dt DATETIME = '2025-10-02 14:23:55';

-- Convert to varchar with style
SELECT CONVERT(VARCHAR, @dt, 103) AS UKFormat; -- dd/MM/yyyy → 02/10/2025
SELECT CONVERT(VARCHAR, @dt, 101) AS USFormat; -- mm/dd/yyyy → 10/02/2025
SELECT FORMAT(@dt, 'dddd, MMMM dd, yyyy hh:mm tt') AS FancyFormat;
```

---

## 6. **Finding Start/End of Period**

```sql
DECLARE @dt DATETIME = '2025-10-02 14:23:55';

-- Start of month
SELECT DATEFROMPARTS(YEAR(@dt), MONTH(@dt), 1) AS StartOfMonth;

-- End of month
SELECT EOMONTH(@dt) AS EndOfMonth;  -- 2025-10-31

-- Start of week (assume week starts Monday)
SELECT DATEADD(DAY, 1 - DATEPART(WEEKDAY, @dt), CAST(@dt AS DATE)) AS StartOfWeek;

-- End of week (Sunday)
SELECT DATEADD(DAY, 7 - DATEPART(WEEKDAY, @dt), CAST(@dt AS DATE)) AS EndOfWeek;
```

---

## 7. **Date Scenarios**

* **Check if a date is weekend**

```sql
SELECT CASE WHEN DATENAME(WEEKDAY, @dt) IN ('Saturday','Sunday') 
            THEN 'Weekend' ELSE 'Weekday' END;
```

* **Age Calculation**

```sql
DECLARE @dob DATE = '1990-06-15';
SELECT DATEDIFF(YEAR, @dob, GETDATE()) 
       - CASE WHEN FORMAT(@dob, 'MMdd') > FORMAT(GETDATE(), 'MMdd') THEN 1 ELSE 0 END 
       AS Age;
```

* **Working Days Between Two Dates**

```sql
DECLARE @start DATE = '2025-10-01', @end DATE = '2025-10-10';
SELECT COUNT(*) AS WorkingDays
FROM (
   SELECT DATEADD(DAY, n, @start) AS d
   FROM (SELECT TOP (DATEDIFF(DAY, @start, @end) + 1) ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) - 1 AS n
         FROM sys.objects) AS Numbers
   WHERE DATENAME(WEEKDAY, DATEADD(DAY, n, @start)) NOT IN ('Saturday','Sunday')
) AS WorkDays;
```

---

## 8. **Time Zone Handling (with DATETIMEOFFSET)**

```sql
DECLARE @dt DATETIMEOFFSET = SYSDATETIMEOFFSET();

-- Convert to another time zone (example: +05:30 IST)
SELECT SWITCHOFFSET(@dt, '+05:30') AS IST_Time;

-- Get UTC
SELECT TODATETIMEOFFSET(SYSDATETIME(), 0) AS UTC_Time;
```

---
