# **Library Management System: C++ to Python Port**

This project demonstrates a complete Library Management System implemented in two different programming languages. It was originally developed in **C++** using low-level data structures and then ported to **Python** to utilize modern data handling and object-oriented principles.

## **Overview**

The system manages a book inventory, handles student borrowing/returning logic, calculates overdue fines, and maintains a waitlist for popular titles.

**Technical Evolution**

| Feature | Original C++ Implementation | Ported Python Implementation |
| :---- | :---- | :---- |
| Data Structure | Manual Linked List (Pointers) | Built-in Dynamic Lists & Objects |
| Waitlist | std::queue | List-based Queueing |
| Storage | Raw .txt file (Line-based) | Structured .json Database |
| Date Logic | Manual Day/Month/Year Math | datetime & timedelta libraries |
| Safety | Manual Memory Management | Automatic Garbage Collection |

## **Key Features**

* **Persistent Storage:** Data is saved automatically and reloaded upon restart.  
* **Smart Borrowing:** Prevents a student from borrowing multiple books at once.  
* **Automatic Fines:** Calculates a $5/day fine for overdue returns.  
* **Waitlist System:** If a book is issued, users can join a queue; the book is automatically assigned to them upon return.

  ## **How to Run**

1. Ensure you have Python 3.x installed.  
2. Run the script via terminal:  
   Bash  
   python library\_system.py  
 


