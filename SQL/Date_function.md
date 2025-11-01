Here’s a **comprehensive SQL practice setup** to help you **master all types of DATE functions** — perfect for interview preparation.
This includes:

* Database creation
* Table creation with multiple date-related columns
* 30+ sample records
* Examples of all major **SQL Server DATE functions** (can adapt easily for MySQL/PostgreSQL too).

---

### 🧱 **Step 1: Create Database**

```sql
CREATE DATABASE DateFunctionPractice;
GO

USE DateFunctionPractice;
GO
```

---

### 🧮 **Step 2: Create Table with Multiple Date Columns**

```sql
CREATE TABLE EmployeeAttendance (
    EmpID INT IDENTITY(1,1) PRIMARY KEY,
    EmpName VARCHAR(50),
    Department VARCHAR(30),
    JoiningDate DATE,
    BirthDate DATE,
    AttendanceDate DATETIME,
    ExitDate DATETIME
);
```

---

### 📥 **Step 3: Insert Sample Data (30 Rows)**

```sql
INSERT INTO EmployeeAttendance (EmpName, Department, JoiningDate, BirthDate, AttendanceDate, ExitDate)
VALUES
('Amit', 'IT', '2020-01-10', '1995-05-15', '2024-10-01 09:00:00', '2024-10-01 18:00:00'),
('Rita', 'HR', '2019-03-22', '1990-07-12', '2024-10-02 09:30:00', '2024-10-02 18:15:00'),
('John', 'Finance', '2018-07-10', '1988-03-02', '2024-10-03 08:45:00', '2024-10-03 17:55:00'),
('Priya', 'IT', '2021-11-05', '1996-11-09', '2024-10-04 09:10:00', '2024-10-04 18:10:00'),
('Raj', 'Sales', '2017-09-17', '1993-01-25', '2024-10-05 09:00:00', '2024-10-05 18:05:00'),
('Sita', 'HR', '2020-12-12', '1992-02-20', '2024-10-06 09:25:00', '2024-10-06 18:20:00'),
('Arjun', 'IT', '2016-08-20', '1989-10-11', '2024-10-07 08:50:00', '2024-10-07 17:45:00'),
('Kavita', 'Finance', '2022-02-15', '1998-05-30', '2024-10-08 09:05:00', '2024-10-08 18:00:00'),
('Sunil', 'Sales', '2019-05-25', '1991-09-14', '2024-10-09 09:00:00', '2024-10-09 18:05:00'),
('Meena', 'HR', '2020-04-10', '1994-08-18', '2024-10-10 09:40:00', '2024-10-10 18:30:00'),
('Ramesh', 'IT', '2018-06-01', '1987-04-04', '2024-10-11 08:55:00', '2024-10-11 17:50:00'),
('Sneha', 'Sales', '2021-01-20', '1995-12-01', '2024-10-12 09:10:00', '2024-10-12 18:15:00'),
('Deepak', 'Finance', '2017-07-07', '1989-07-07', '2024-10-13 09:05:00', '2024-10-13 17:55:00'),
('Manisha', 'IT', '2023-03-10', '2000-03-15', '2024-10-14 09:25:00', '2024-10-14 18:10:00'),
('Vijay', 'Sales', '2015-11-21', '1985-05-19', '2024-10-15 09:00:00', '2024-10-15 18:00:00'),
('Rohit', 'Finance', '2020-09-01', '1993-09-05', '2024-10-16 08:45:00', '2024-10-16 17:45:00'),
('Kiran', 'HR', '2016-10-10', '1988-12-22', '2024-10-17 09:00:00', '2024-10-17 18:00:00'),
('Nisha', 'IT', '2019-04-04', '1992-10-12', '2024-10-18 09:15:00', '2024-10-18 18:05:00'),
('Harsh', 'Sales', '2021-06-19', '1997-02-09', '2024-10-19 09:30:00', '2024-10-19 18:30:00'),
('Pooja', 'Finance', '2018-05-05', '1991-11-11', '2024-10-20 08:50:00', '2024-10-20 17:50:00'),
('Anil', 'IT', '2017-12-25', '1986-01-20', '2024-10-21 09:00:00', '2024-10-21 18:00:00'),
('Geeta', 'HR', '2020-06-15', '1995-03-25', '2024-10-22 09:10:00', '2024-10-22 18:05:00'),
('Mahesh', 'Finance', '2019-07-30', '1990-08-17', '2024-10-23 08:55:00', '2024-10-23 17:50:00'),
('Alok', 'Sales', '2018-09-09', '1988-09-09', '2024-10-24 09:05:00', '2024-10-24 18:10:00'),
('Lata', 'IT', '2022-01-14', '1999-04-14', '2024-10-25 09:20:00', '2024-10-25 18:20:00'),
('Tina', 'Finance', '2016-11-11', '1987-11-11', '2024-10-26 09:00:00', '2024-10-26 18:00:00'),
('Gopal', 'Sales', '2023-04-17', '2000-07-19', '2024-10-27 09:10:00', '2024-10-27 18:15:00'),
('Neha', 'HR', '2021-08-08', '1996-02-05', '2024-10-28 09:30:00', '2024-10-28 18:25:00'),
('Vivek', 'IT', '2019-02-19', '1993-12-23', '2024-10-29 09:05:00', '2024-10-29 18:05:00'),
('Rekha', 'Finance', '2017-03-03', '1989-03-03', '2024-10-30 08:45:00', '2024-10-30 17:45:00');
```

---

### 🧩 **Step 4: Practice Date Functions**

#### 1. **GETDATE()** → Current system date/time

```sql
SELECT GETDATE() AS CurrentDateTime;
```

#### 2. **SYSDATETIME()**

```sql
SELECT SYSDATETIME() AS CurrentSystemDateTime;
```

#### 3. **DATEPART()** → Extract part of date

```sql
SELECT EmpName, DATEPART(YEAR, JoiningDate) AS JoiningYear, DATEPART(MONTH, JoiningDate) AS JoiningMonth FROM EmployeeAttendance;
```

#### 4. **DATENAME()** → Get textual date parts

```sql
SELECT EmpName, DATENAME(WEEKDAY, AttendanceDate) AS DayName FROM EmployeeAttendance;
```

#### 5. **DAY(), MONTH(), YEAR()**

```sql
SELECT EmpName, DAY(BirthDate) AS BirthDay, MONTH(BirthDate) AS BirthMonth, YEAR(BirthDate) AS BirthYear FROM EmployeeAttendance;
```

#### 6. **DATEADD()** → Add/Subtract days, months, years

```sql
SELECT EmpName, DATEADD(DAY, 10, JoiningDate) AS JoiningPlus10Days FROM EmployeeAttendance;
```

#### 7. **DATEDIFF()** → Difference between two dates

```sql
SELECT EmpName, DATEDIFF(YEAR, JoiningDate, GETDATE()) AS YearsWorked FROM EmployeeAttendance;
```

#### 8. **EOMONTH()** → Last day of month

```sql
SELECT EmpName, EOMONTH(JoiningDate) AS MonthEndDate FROM EmployeeAttendance;
```

#### 9. **FORMAT()** → Custom date formatting

```sql
SELECT EmpName, FORMAT(JoiningDate, 'dd-MMM-yyyy') AS FormattedJoiningDate FROM EmployeeAttendance;
```

#### 10. **ISDATE()** → Validate if value is a date

```sql
SELECT ISDATE('2025-01-01') AS IsValidDate, ISDATE('invalid-date') AS InvalidCheck;
```

#### 11. **CONVERT()** → Convert date format

```sql
SELECT EmpName, CONVERT(VARCHAR(20), JoiningDate, 103) AS DateInDDMMYYYY FROM EmployeeAttendance;
```

#### 12. **CAST()** → Convert type

```sql
SELECT CAST(JoiningDate AS DATETIME) AS JoiningDateTime FROM EmployeeAttendance;
```

#### 13. **DATEFROMPARTS()**

```sql
SELECT DATEFROMPARTS(2024, 12, 25) AS XmasDate;
```

#### 14. **SWITCHOFFSET()** (Time zone adjustment)

```sql
SELECT SYSDATETIMEOFFSET(), SWITCHOFFSET(SYSDATETIMEOFFSET(), '+05:30') AS IndiaTime;
```

#### 15. **TODATETIMEOFFSET()**

```sql
SELECT TODATETIMEOFFSET('2024-10-20 10:00:00', '+05:30') AS WithOffset;
```

#### 16. **CURRENT_TIMESTAMP** (same as GETDATE)

```sql
SELECT CURRENT_TIMESTAMP AS CurrentTimeStamp;
```

#### 17. **DATE_TRUNC()** (SQL Server 2022+ / Postgres)

```sql
SELECT DATE_TRUNC('month', AttendanceDate) AS MonthStart FROM EmployeeAttendance;
```

#### 18. **LEAP YEAR check**

```sql
SELECT EmpName, YEAR(BirthDate) AS YearOfBirth,
       CASE WHEN (YEAR(BirthDate) % 4 = 0 AND (YEAR(BirthDate) % 100 <> 0 OR YEAR(BirthDate) % 400 = 0))
            THEN 'Leap Year' ELSE 'Not Leap Year' END AS LeapCheck
FROM EmployeeAttendance;
```

---

### 🎯 **Bonus: Realistic Scenarios**

* Employees joined in the **last 2 years**:

```sql
SELECT EmpName, JoiningDate
FROM EmployeeAttendance
WHERE DATEDIFF(YEAR, JoiningDate, GETDATE()) <= 2;
```

* Birthdays this **month**:

```sql
SELECT EmpName, BirthDate
FROM EmployeeAttendance
WHERE MONTH(BirthDate) = MONTH(GETDATE());
```

* Attendance **on weekends**:

```sql
SELECT EmpName, AttendanceDate, DATENAME(WEEKDAY, AttendanceDate) AS DayName
FROM EmployeeAttendance
WHERE DATENAME(WEEKDAY, AttendanceDate) IN ('Saturday','Sunday');
```

---

Would you like me to generate a **MySQL** or **PostgreSQL** version of this too (with equivalent functions)?
Here’s a **comprehensive SQL practice setup** to help you **master all types of DATE functions** — perfect for interview preparation.