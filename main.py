from fastmcp import FastMCP
import os
import sqlite3


db_path = os.path.join(os.path.dirname(__file__),"calendar.db")
categories_path = os.path.join(os.path.dirname(__file__),"catergories.json")
mcp = FastMCP("calender")

def init_db():
    with sqlite3.connect(db_path) as c:
        c.execute("""
                CREATE TABLE IF NOT EXISTs calendar(
                    id integer primary key autoincrement,
                    date text not null,
                    categories text not null,
                    event text not null,
                    note text default ''
                  )
                  """)
init_db()

@mcp.tool
def add_event(date, event , category, note=""):
    '''add a new event entery to the data base with description'''
    with sqlite3.connect(db_path) as c:
        cur = c.execute(
            """insert into calendar (date ,categories, event , note) values (?,?,?,?)""",
            (date ,category, event, note)
        )
        return {'status':"ok", "id":cur.lastrowid}

@mcp.tool()
def list_events(start_date , end_date):
    '''list the events remaining from a given date to the date mentioned or all the events ahead'''
    with sqlite3.connect(db_path) as c:
        cur = c.execute(
            """select * from calendar where date between ? and ? order by id asc""",
            (start_date , end_date)
        )
        cols = [e[0] for e in cur.description]
        return [dict(zip(cols,r)) for r in cur.fetchall()]

@mcp.resource("calendar://categories")
def categories():
    with open(categories_path , "r" , encoding="utf-8") as f:
        return f.read()


if __name__ == "__main__":
    mcp.run()
