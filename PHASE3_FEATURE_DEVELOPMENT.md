# Phase 3: Feature Development Plan

## 📋 Overview

เป้าหมาย: พัฒนา features ใหม่เพื่อเพิ่มประสบการณ์ผู้ใช้

---

## Features to Implement

### 1. Real-time Gold Price Updates (WebSocket) 🔴 Priority High
**Backend:**
- [x] GoldPriceConsumer อยู่แล้ว (ต้อง register ใน routing.py)
- [ ] สร้าง service สำหรับ broadcast price updates
- [ ] เพิ่ม management command สำหรับ simulate price updates

**Frontend:**
- [ ] สร้าง WebSocket hook (`useGoldPriceWebSocket`)
- [ ] อัปเดต Dashboard ให้แสดงราคา real-time
- [ ] แสดง animation เมื่อราคาเปลี่ยน (สีเขียว/แดง)

### 2. Price Alerts 🔔 Priority High
**Backend:**
- [ ] สร้าง PriceAlert model
- [ ] สร้าง API endpoints (CRUD)
- [ ] สร้าง service ตรวจสอบ alerts เมื่อราคาเปลี่ยน
- [ ] ส่ง notification ผ่าน WebSocket เมื่อ trigger

**Frontend:**
- [ ] หน้าจัดการ Price Alerts
- [ ] Form สร้าง/แก้ไข alerts
- [ ] แสดง notification เมื่อ alert triggered

### 3. Portfolio Analytics & Charts 📊 Priority Medium
**Frontend:**
- [ ] กราฟราคาทองย้อนหลัง (Line chart)
- [ ] กราฟ portfolio performance
- [ ] สรุป profit/loss
- [ ] ใช้ Chart.js หรือ Recharts

### 4. Push Notifications 📱 Priority Low
- [ ] Browser push notifications
- [ ] Service Worker setup
- [ ] Notification preferences

---

## Team Assignment

| Feature | Owner | Model |
|---------|-------|-------|
| WebSocket Backend | คุณฐาน | glm-4.7 |
| WebSocket Frontend + Charts | คุณอาร์ต | glm-4.5 |
| Price Alerts | คุณฐาน | glm-4.7 |

---

## Timeline

| Day | Task | Owner |
|-----|------|-------|
| Today | WebSocket routing + Frontend hook | ฐาน + อาร์ต |
| Today | Price charts integration | อาร์ต |
| Today | Price Alerts API | ฐาน |

---

*Created: 5 Feb 2026*
