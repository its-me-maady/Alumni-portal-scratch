# 📌 Database Schema

This document defines the database schema for the project.

---

## 🛠️ **Admin Table**

| Field      | Type         | Constraints                 |
| ---------- | ------------ | --------------------------- |
| `id`       | Integer      | Primary Key, Auto Increment |
| `email`    | String (255) | Unique, Not Null            |
| `password` | String (255) | Not Null                    |

---

## 👤 **User Table**

| Field          | Type         | Constraints                 |
| -------------- | ------------ | --------------------------- |
| `register_no`  | Integer      | Primary Key, Not Null       |
| `name`         | String (100) | Not Null                    |
| `password`     | String (255) | Not Null                    |
| `job_position` | String (100) | Optional                    |
| `year`         | Integer      | Not Null                    |
| `dept`         | String (100) | Not Null                    |
| `email`        | String (120) | Unique, Not Null            |
| `whatsapp_no`  | String (20)  | Unique, Optional            |
| `photo`        | String (255) | Path to stored photo        |
| `date_active`  | DateTime     | Defaults to `NOW()`         |
| `active_hours` | String (50)  | Example: `"9 AM - 5 PM"`    |

---

## 🎉 **Events Table**

| Field         | Type         | Constraints                 |
| ------------- | ------------ | --------------------------- |
| `id`          | Integer      | Primary Key, Auto Increment |
| `title`       | String (200) | Not Null                    |
| `description` | Text         | Not Null                    |
| `expiry_date` | DateTime     | Not Null                    |
| `photos`      | String (255) | Path to stored photos       |

---

## 🔗 **User_Event Table (Junction)**

| Field      | Type    | Constraints           |
| ---------- | ------- | -------------------- |
| `user_id`  | Integer | Primary Key, Foreign Key (User.register_no) |
| `event_id` | Integer | Primary Key, Foreign Key (Event.id) |

✅ **Relationships:**
- User ↔️ Event: Many-to-Many through user_event table
- Event.interested_users: List of users interested in the event
- User.interested_events: List of events user is interested in

✅ **Additional Features:**
- `is_expired()`: A method to check if an event has expired based on the `expiry_date`
