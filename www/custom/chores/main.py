import sqlite3
import datetime
import json
import calendar
from enum import Enum

DB_FILEPATH = "www/custom/chores/chores.db"

class ChoreTable(Enum):
    ID = "id"                       # integer, auto-assigned
    TITLE = "title"                 # text, mandatory
    DESCRIPTION = "description"     # text, optional
    INSTRUCTIONS = "instructions"   # text, optional
    TYPE = "type"                   # text, mandatory
    CYCLE = "cycle"                 # integer, choose one
    WEEKLY_DAY = "weekly_day"       # integer, choose one
    MONTHLY_DAY = "monthly_day"     # integer, choose one
    YEARLY_DATE = "yearly_date"     # date, choose one
    PREV_EXEC = "prev_exec"         # integer, auto-assigned
    NEXT_DUE = "next_due"           # datetime, auto-assigned
    TIME_ESTIMATE = "time_estimate" # integer, optional
    CATEGORY = "category"           # text, mandatory
    SCORE = "score"                 # integer, optional
    PRIORITY = "priority"           # integer, optional

class ExecutionTable(Enum):
    ID = "id"                       # integer, auto-assigned
    CHORE = "chore"                 # integer, mandatory
    TIMESTAMP = "timestamp"         # datetime, mandatory
    DAYS_TO_DUE = "days_to_due"     # integer, auto-assigned
    PERFORMED_BY = "performed_by"   # text, optional
    TIME_SPENT = "time_spent"       # integer, optional
    COMMENT = "comment"             # text, optional
    SCORE_AWARDED = "score_awarded" # integer, auto-assigned

class ChoreType(Enum):
    CYCLIC = "cyclic"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"

class ChoreState(Enum):
    PENDING = "pending"
    OVERDUE = "overdue"

class ChoreCategory(Enum):
    HOUSE = "house"
    WORK = "work"
    SEASONAL = "seasonal"
    CAR = "car"
    PERSONAL = "personal"
    OTHER = "other"

'''
 table chore:
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        instructions TEXT,        
        type TEXT NOT NULL,
        cycle INTEGER DEFAULT 7,
        weekly_day INTEGER DEFAULT 7,
        monthly_day INTEGER DEFAULT 1,
        yearly_date DATETIME,
        prev_exec INTEGER,
        next_due DATETIME,
        time_estimate INTEGER,
        category TEXT NOT NULL DEFAULT 'house',
        score INTEGER,
        priority INTEGER DEFAULT 5,
        FOREIGN KEY (prev_exec) REFERENCES execution (id)
'''

'''
Table chore does not need to include field "state", as this can be calculated upon
request by comparing next_due with current date. It also requires an update of all entries
regulary.
'''

'''
table execution:
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chore INTEGER NOT NULL,
        timestamp DATETIME NOT NULL,
        days_to_due INTEGER,
        performed_by TEXT,
        time_spent INTEGER,
        comment TEXT,
        score_awarded INTEGER,
        FOREIGN KEY (chore) REFERENCES chore (id)
'''

def create_chore(title: str, type="cyclic", cycle: int = 7, weekly_day: int = 7,
                 monthly_day: int = 1, yearly_date: str = "2024-01-01", category="house", 
                 priority=5, score: int = 0, description: str = "", instructions: str = ""):
     
     prev_exec = 0
     next_due = calculate_next_due(type, datetime.date.today(), cycle, weekly_day, monthly_day, yearly_date)
     
     conn = sqlite3.connect(DB_FILEPATH)
     c = conn.cursor()

     c.execute('''INSERT INTO chore (title, description, instructions, type, cycle, weekly_day, monthly_day, yearly_date, prev_exec, next_due, category, priority, score)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (title, description, instructions, type, cycle, weekly_day, monthly_day, yearly_date, prev_exec, next_due, category, priority, score))

     conn.commit()
     conn.close()


def update_chore_field(chore_id: int, field: ChoreTable, value):
    conn = sqlite3.connect(DB_FILEPATH)
    c = conn.cursor()

    c.execute(f"UPDATE chore SET {field.value} = ? WHERE id = ?", (value, chore_id))

    conn.commit()
    conn.close()


def get_chore(chore_id: int):
    conn = sqlite3.connect(DB_FILEPATH)
    c = conn.cursor()

    c.execute('''SELECT id, title, description, instructions, type, cycle, weekly_day, monthly_day, yearly_date,
                        prev_exec, next_due, time_estimate, category, score, priority FROM chore
                        WHERE id = ?''', (chore_id,))

    row = c.fetchone()

    if row is None:
        return None

    chore_id, title, description, instructions, chore_type, cycle, weekly_day, monthly_day, yearly_date, \
    prev_exec, next_due, time_estimate, category, score, priority = row

    next_due = format_string_datetime(next_due)
    current_datetime = datetime.datetime.now()

    state = calculate_chore_state(next_due, current_datetime)
    time_left = calculate_time_left(next_due, current_datetime)
    pcnt_left = calculate_percentage_left(time_left, cycle)

    chore_data = {
        "id": chore_id,
        "title": title,
        "description": description,
        "instructions": instructions,
        "type": chore_type,
        "cycle": cycle,
        "weekly_day": weekly_day,
        "monthly_day": monthly_day,
        "yearly_date": yearly_date,
        "prev_exec": prev_exec,
        "next_due": next_due.strftime("%Y-%m-%d %H:%M:%S"),
        "time_estimate": time_estimate,
        "category": category,
        "score": score,
        "priority": priority,
        "state": state,
        "time_left": time_left,
        "pcnt_left": pcnt_left
    }

    return json.dumps(chore_data)

# Deletes a chore from the database
def delete_chore(chore_id: int):
    conn = sqlite3.connect(DB_FILEPATH)
    c = conn.cursor()

    c.execute("DELETE FROM chore WHERE id = ?", (chore_id,))

    conn.commit()
    conn.close()

# Returns a list of chores ordered by next_due date
def get_chore_list(items: int = 25):
    conn = sqlite3.connect(DB_FILEPATH)
    c = conn.cursor()

    c.execute('''SELECT id, title, type, cycle, weekly_day, monthly_day, yearly_date, next_due FROM chore
                    ORDER BY next_due ASC LIMIT ?''', (items,))

    chores = []
    current_datetime = datetime.datetime.now()

    for row in c.fetchall():
        chore_id, title, chore_type, cycle, weekly_day, monthly_day, yearly_date, next_due = row
        next_due = format_string_datetime(next_due)
        time_left = calculate_time_left(next_due, current_datetime)
        pcnt_left = calculate_percentage_left(chore_type, cycle, time_left)

        chore_state = calculate_chore_state(next_due, current_datetime)

        chore = {
            "id": chore_id,
            "title": title,
            "type": chore_type,
            "type_value": choose_type_value(chore_type, cycle, weekly_day, monthly_day, yearly_date),
            "next_due": next_due.strftime("%Y-%m-%d %H:%M:%S"),
            "state": chore_state,
            "time_left": time_left,
            "pcnt_left": pcnt_left
        }

        chores.append(chore)

    conn.close()

    return json.dumps(chores)

# Returns how many hours are left between the ref_datetime and next_due
def calculate_time_left(next_due: datetime.datetime, ref_datetime: datetime.datetime):
    time_left = (next_due - ref_datetime).total_seconds() / 3600
    time_left = round(time_left)
    if time_left < 0:
        time_left = 0
    return time_left

# Returns the percentage of time left relative to the chore type
def calculate_percentage_left(chore_type: str, cycle: int, time_left: int):
    if chore_type == ChoreType.CYCLIC.value:
        percentage_left = round((time_left / (cycle * 24)) * 100)
    elif chore_type == ChoreType.WEEKLY.value:
        percentage_left = round((time_left / (7 * 24)) * 100)
    elif chore_type == ChoreType.MONTHLY.value:
        percentage_left = round((time_left / (31 * 24)) * 100)
    elif chore_type == ChoreType.YEARLY.value:
        percentage_left = round((time_left / (365 * 24)) * 100)

    if percentage_left > 100:
        return 100

    return percentage_left

'''
Utility functions
'''

def choose_type_value(type: str, cycle: int, weekly_day: int, monthly_day: int, yearly_date: str):
    if type == ChoreType.CYCLIC.value:
        return cycle
    elif type == ChoreType.WEEKLY.value:
        return weekly_day
    elif type == ChoreType.MONTHLY.value:
        return monthly_day
    elif type == ChoreType.YEARLY.value:
        return yearly_date

# Determines the state of a chore based on the next_due date
def calculate_chore_state(next_due: datetime.datetime, ref_datetime: datetime.datetime):
    if next_due < ref_datetime:
        return ChoreState.OVERDUE.value
    else:
        return ChoreState.PENDING.value



def calculate_next_due(chore_type: str, reference_date: datetime.date, cycle: int = None,
                       weekly_day: int = None, monthly_day: int = None, yearly_date: str = None):
    
    reference_time = datetime.datetime.combine(reference_date, datetime.time(12, 0))
    
    # Cyclic
    if chore_type == ChoreType.CYCLIC.value:
        return calculate_next_cyclic(reference_time, cycle)
    
    # Weekly
    elif chore_type == ChoreType.WEEKLY.value:
        return calculate_next_weekly(reference_time, weekly_day)
    
    # Monthly
    elif chore_type == ChoreType.MONTHLY.value:
       return calculate_next_monthly(reference_time, monthly_day)
    
    # Yearly
    elif chore_type == ChoreType.YEARLY.value:
        return calculate_next_yearly(reference_time, format_string_date(yearly_date))

def calculate_next_cyclic(ref: datetime.datetime, cycle: int):
    return ref + datetime.timedelta(days=cycle)

def calculate_next_weekly(ref: datetime.datetime, weekly_day: int):
    ref_weekday = ref.isoweekday()
    if weekly_day == ref_weekday:
        days_until_next_day = 7
    else:
        days_until_next_day = (weekly_day - ref_weekday + 7) % 7
    return ref + datetime.timedelta(days=days_until_next_day)
    
def calculate_next_monthly(ref: datetime.datetime, monthly_day: int):
    
    # Get the last day of this month
    last_day_of_month = calendar.monthrange(ref.year, ref.month)[1]
    
    # Truncate monthly_day if it exceeds the last day of the month
    if monthly_day > last_day_of_month:
        monthly_day = last_day_of_month
        
        
    # Check if it is at or past the monthly_day of this month
    # Find the monthly_day of next month, as well as year and month
    if ref.day >= monthly_day:
         
        # Calculate the next month
        if ref.month == 12:
            next_month = 1
            next_year = ref.year + 1
        else:
            next_month = ref.month + 1
            next_year = ref.year
            
        # Find the last day of the next month
        last_day_of_month = calendar.monthrange(next_year, next_month)[1]
        
        if monthly_day > last_day_of_month:
            monthly_day = last_day_of_month
            
    # It is this month, so just use the current month and year and the monthly_day
    else:
        next_month = ref.month
        next_year = ref.year
    
    # Calculate the next occurrence of the monthly_day
    next_due_date = datetime.date(next_year, next_month, monthly_day)
    
    # Add time to the next_due_date
    next_due_time = datetime.time(12, 0)
    next_due_datetime = datetime.datetime.combine(next_due_date, next_due_time)
    
    return next_due_datetime

def calculate_next_yearly(ref: datetime.datetime, yearly_date: datetime.date):
        
        # Check if it is at or past the yearly_date of this year
        # Find the yearly_date of next year, as well as year
        if ref.month > yearly_date.month:
            next_year = ref.year + 1 
        elif ref.month == yearly_date.month and ref.day >= yearly_date.day:
            next_year = ref.year + 1
        else:
            next_year = ref.year
            
        if yearly_date.month == 2 and yearly_date.day == 29:
            # Check if next_year is a leap year
            if not calendar.isleap(next_year):
                yearly_date = datetime.date(next_year, 2, 28)
        
        # Calculate the next occurrence of the yearly_date
        next_due_date = datetime.date(next_year, yearly_date.month, yearly_date.day)
        
        # Add time to the next_due_date
        next_due_time = datetime.time(12, 0)
        next_due_datetime = datetime.datetime.combine(next_due_date, next_due_time)
        
        return next_due_datetime

def format_string_date(date: str):
    return datetime.datetime.strptime(date, "%Y-%m-%d")

def format_string_datetime(dt: str):
    return datetime.datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")

'''
Executions
'''

# The quickest way to add an execution, using the current time, and skips performed_by and comment
def quick_add_execution(chore_id: int):

    conn = sqlite3.connect(DB_FILEPATH)
    cursor = conn.cursor()

    # Retrieve next_due, type, cycle, weekly_day, monthly_day, yearly_date, and score from chore table
    cursor.execute("SELECT next_due, type, cycle, weekly_day, monthly_day, yearly_date, score FROM chore WHERE id = ?", (chore_id,))
    result = cursor.fetchone()
    next_due, chore_type, cycle, weekly_day, monthly_day, yearly_date, score = result

    # Get current date and time
    timestamp = datetime.datetime.now()
    
    # Convert next_due to datetime object
    next_due = format_string_datetime(next_due)

    # Calculate days_to_due
    days_to_due = (next_due - timestamp).days

    # Calculate the next due date using the calculate_next_due function
    next_due = calculate_next_due(chore_type, next_due.date(), cycle, weekly_day, monthly_day, yearly_date)

    # Insert new row into execution table
    cursor.execute("INSERT INTO execution (chore, timestamp, days_to_due, performed_by, score_awarded) VALUES (?, ?, ?, NULL, ?)",
                   (chore_id, timestamp, days_to_due, score))
    execution_id = cursor.lastrowid

    # Update prev_exec and next_due in chore table
    cursor.execute("UPDATE chore SET prev_exec = ?, next_due = ? WHERE id = ?", (execution_id, next_due, chore_id))

    conn.commit()
    conn.close()
    

# The comprehensive way of adding an execution, using some given timestamp, performed by someone, and with a comment
def add_execution(chore_id: int, timestamp: datetime.datetime, performed_by: str, comment: str = None):

    conn = sqlite3.connect(DB_FILEPATH)
    cursor = conn.cursor()

    cursor.execute("SELECT next_due, type, cycle, weekly_day, monthly_day, yearly_date, score FROM chore WHERE id = ?", (chore_id,))
    result = cursor.fetchone()
    next_due, chore_type, cycle, weekly_day, monthly_day, yearly_date, score = result

    next_due = format_string_datetime(next_due)

    days_to_due = (next_due - timestamp).days

    # Calculate the next due date using the calculate_next_due function
    next_due = calculate_next_due(chore_type, timestamp, cycle, weekly_day, monthly_day, yearly_date)

    # Insert new row into execution table
    cursor.execute("INSERT INTO execution (chore, timestamp, days_to_due, performed_by, score_awarded, comment) VALUES (?, ?, ?, ?, ?, ?)",
                   (chore_id, timestamp, days_to_due, performed_by, score, comment))
    execution_id = cursor.lastrowid

    # Update prev_exec and next_due in chore table
    cursor.execute("UPDATE chore SET prev_exec = ?, next_due = ? WHERE id = ?", (execution_id, next_due, chore_id))

    conn.commit()
    conn.close()


print(get_chore_list(20))  
#print("")
#print(get_chore(2))
#print(calculate_next_due("weekly", format_string_date("2024-01-08"), 7, 1, 1, "2021-01-01 12:00:00")))
#print(calculate_next_monthly(format_string_date("2024-02-02"), 30))
#print(calculate_next_yearly(datetime.date(2024, 3, 10), datetime.date(2020, 5, 7)))
#create_chore("Pynte til jul", "yearly", yearly_date="2024-11-06", category="house", instructions="Hente dedikert eske på loftet som all pynt skal i. Plasttreet går for seg selv i loftsboden. Julepapir legges sammen med annet gavepapir.")
#update_chore_field(4, ChoreTable.NEXT_DUE, "2024-01-06 12:00:00")
#quick_add_execution(4)
#print(calculate_next_due("cyclic", format_string_date("2024-01-06"), cycle=28))