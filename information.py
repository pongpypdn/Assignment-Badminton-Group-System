import streamlit as st  # นำเข้าไลบรารีสำหรับสร้าง Web Interface
import sqlite3          # นำเข้าไลบรารีสำหรับจัดการฐานข้อมูล SQL
import random           # นำเข้าไลบรารีสำหรับสุ่มข้อมูล (ใช้สุ่มคู่)
import pandas as pd     # นำเข้าไลบรารีสำหรับจัดการข้อมูลในรูปแบบตารางและ CSV

# ฟังก์ชันแสดงหน้าต่างป๊อปอัพสำหรับแก้ไขข้อมูลสมาชิก
@st.dialog("แก้ไขข้อมูลสมาชิก")
def edit_member_dialog(name, lv, phone):
    st.write(f"กำลังแก้ไขข้อมูลคุณ: **{name}**")  # แสดงชื่อที่กำลังแก้ไข
    with st.expander("✏️ แก้ไขชื่อ"):  # ส่วนพับสำหรับแก้ไขชื่อ
        new_name = st.text_input("ชื่อใหม่", value=name)  # ช่องรับชื่อใหม่
        if st.button("บันทึกชื่อ"):  # ปุ่มบันทึกการเปลี่ยนชื่อ
            db.cursor.execute("UPDATE members SET name = ? WHERE name = ?", (new_name, name))  # อัปเดตชื่อในตารางสมาชิก
            db.cursor.execute("UPDATE expenses SET member_name = ? WHERE member_name = ?", (new_name, name))  # อัปเดตชื่อในตารางค่าใช้จ่ายด้วย
            db.conn.commit()  # ยืนยันการเปลี่ยนแปลงลงฐานข้อมูล
            st.rerun()  # รีเฟรชหน้าเว็บ

    with st.expander("📞 แก้ไขเบอร์โทร"):  # ส่วนพับสำหรับแก้ไขเบอร์โทร
        new_phone = st.text_input("เบอร์ใหม่", value=phone, max_chars=10)  # ช่องรับเบอร์ใหม่
        if st.button("บันทึกเบอร์"):  # ปุ่มบันทึกเบอร์โทร
            db.cursor.execute("UPDATE members SET phone = ? WHERE name = ?", (new_phone, name))  # อัปเดตเบอร์ในฐานข้อมูล
            db.conn.commit()  # ยืนยันการเปลี่ยนแปลง
            st.rerun()  # รีเฟรชหน้าเว็บ

    with st.expander("🏆 แก้ไขระดับ"):  # ส่วนพับสำหรับแก้ไขระดับฝีมือ
        new_lv = st.radio("เลือกระดับใหม่", ["BG", "N-", "N", "NS", "S", "P-", "P" ], index=lv-1, horizontal=True)  # ตัวเลือกเลเวลใหม่
        if st.button("บันทึกระดับ"):  # ปุ่มบันทึกเลเวล
            # แปลงชื่อเลเวลกลับเป็นตัวเลข (หา index จาก list แล้วบวก 1)
            lv_val = ["BG", "N-", "N", "NS", "S", "P-", "P"].index(new_lv) + 1
            db.cursor.execute("UPDATE members SET level = ? WHERE name = ?", (lv_val, name))  # อัปเดตเลเวลในฐานข้อมูล
            db.conn.commit()  # ยืนยันการเปลี่ยนแปลง
            st.rerun()  # รีเฟรชหน้าเว็บ

# ฟังก์ชันแสดงหน้าต่างป๊อปอัพยืนยันการลบ
@st.dialog("⚠️ ยืนยันการลบสมาชิก")
def delete_confirm_dialog(name):
    st.write(f"คุณต้องการลบข้อมูลของคุณ **{name}** ใช่หรือไม่ ?")  # ถามความยืนยัน
    st.write("การลบจะไม่สามารถกู้คืนได้ และจะลบข้อมูลที่เกี่ยวข้องทั้งหมดด้วย")  # คำเตือน
    
    col1, col2 = st.columns(2)  # สร้าง 2 คอลัมน์สำหรับปุ่ม
    if col1.button("ยืนยันการลบ", type="primary"):  # ปุ่มยืนยัน (สีแดง/เด่น)
        db.cursor.execute("DELETE FROM members WHERE name = ?", (name,))  # ลบจากตารางสมาชิก
        db.cursor.execute("DELETE FROM expenses WHERE member_name = ?", (name,))  # ลบจากตารางหนี้สิน
        db.conn.commit()  # ยืนยันการเปลี่ยนแปลง
        st.success("ลบข้อมูลเรียบร้อย")  # แจ้งเตือนสำเร็จ
        st.rerun()  # รีเฟรชหน้าเว็บ
    if col2.button("ยกเลิก"):  # ปุ่มยกเลิก
        st.rerun()  # ปิดหน้าต่างโดยการรีเฟรช

# ตั้งค่าคอนฟิกของหน้าเว็บ (หัวข้อแท็บ, ไอคอน, การวางเลย์เอาต์)
st.set_page_config(page_title="BADMINTON GROUP SYSTEM", page_icon="🏸", layout="wide")

# ฟังก์ชันตั้งค่าฟอนต์ภาษาไทย (Kanit)
def set_custom_font():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500;600&display=swap');
    html, body, [class*="css"], .stApp, .stButton, .stTextInput, .stMarkdown, p, h1, h2, h3, h4, h5, h6 {
        font-family: 'Kanit', sans-serif !important;
    }
    </style>
    """, unsafe_allow_html=True)

set_custom_font()  # เรียกใช้ฟังก์ชันตั้งค่าฟอนต์

# คลาสจัดการระบบหลังบ้านและฐานข้อมูล
class BadmintonWebSystem:
    def __init__(self, db_name="badminton_club.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)  # เชื่อมต่อฐานข้อมูล
        self.cursor = self.conn.cursor()  # สร้าง cursor สำหรับรัน SQL
        # ดิกชันนารีแปลงตัวเลขเป็นชื่อระดับ
        self.level_names = {7: "P", 6: "P-", 5: "S", 4: "NS", 3: "N", 2: "N-", 1: "BG"}
        self._create_tables()  # สร้างตารางเมื่อเริ่มโปรแกรม

    def _create_tables(self):
        # สร้างตารางสมาชิก
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS members (
                name TEXT PRIMARY KEY, 
                level INTEGER, 
                phone TEXT UNIQUE
            )
        ''')
        # สร้างตารางค่าใช้จ่าย/หนี้สิน
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                member_name TEXT,
                item TEXT,
                price REAL,
                FOREIGN KEY (member_name) REFERENCES members(name)
            )
        ''')
        self.conn.commit()  # บันทึกโครงสร้างตาราง

    def get_all_members(self):
        self.cursor.execute("SELECT name, level, phone FROM members")  # ดึงข้อมูลสมาชิกทั้งหมด
        return self.cursor.fetchall()  # ส่งกลับเป็น list ของข้อมูล

    def get_all_expenses(self):
        self.cursor.execute("SELECT member_name, item, price FROM expenses")  # ดึงข้อมูลหนี้สินทั้งหมด
        return self.cursor.fetchall()  # ส่งกลับเป็น list ของข้อมูล

db = BadmintonWebSystem()  # สร้าง Object จากคลาสฐานข้อมูล

# รายการเมนูบน Sidebar
menu_items = ["📊 ภาพรวมระบบ", "👤 จัดการสมาชิก", "💰 จัดการค่าใช้จ่าย", "🎲 สุ่มจับคู่", "💾 สำรองข้อมูล"]

# ตรวจสอบว่ามีตัวแปรเก็บหน้าปัจจุบันใน session หรือยัง
if 'current_page' not in st.session_state:
    st.session_state.current_page = menu_items[0]  # ถ้าไม่มี ให้เริ่มที่หน้าแรก

# ส่วนจัดการ Sidebar (แถบด้านข้าง)
with st.sidebar:
    col1, col2, col3 = st.columns([1, 2, 1])  # แบ่งคอลัมน์เพื่อวางรูปตรงกลาง
    with col2:
        st.image("badminton_kmutnb.png", width=200)  # แสดงรูปโลโก้
    st.markdown("<h2 style='text-align: center;'>BADMINTON GROUP SYSTEM</h2>", unsafe_allow_html=True)  # ชื่อระบบ
    st.caption("<h5 style='text-align: center;'>PROBLEM SOLVING PROJECT</h5>", unsafe_allow_html=True)  # ชื่อโปรเจกต์
    st.markdown("---")  # เส้นคั่น
    st.write("**เมนูควบคุม**")  # หัวข้อเมนู

    for item in menu_items:  # วนลูปสร้างปุ่มเมนู
        if st.button(item, use_container_width=True, type="secondary"):  # ถ้ากดปุ่มเมนู
            st.session_state.current_page = item  # เปลี่ยนหน้าปัจจุบัน
            st.rerun()  # รีเฟรชหน้าจอ
    st.markdown("---")  # เส้นคั่น
    st.caption("<h5 style='text-align: center;'>BADMINTON KMUTNB PRACHINBURI</h5>", unsafe_allow_html=True)  # ชื่อสถาบัน
    choice = st.session_state.current_page  # เก็บค่าหน้าปัจจุบันไว้ในตัวแปร choice

# --- เนื้อหาแต่ละหน้า (Choice) ---

if choice == "📊 ภาพรวมระบบ":
    st.subheader("📊 ภาพรวมระบบ")  # หัวข้อหน้า
    st.markdown("---")
    members = db.get_all_members()  # ดึงสมาชิกทั้งหมด
    expenses = db.get_all_expenses()  # ดึงค่าใช้จ่ายทั้งหมด

    col1, col2, col3 = st.columns(3)  # สร้าง 3 คอลัมน์แสดงสถิติ
    with col1:
        st.subheader("จำนวนสมาชิกทั้งหมด")
        st.info(f"{len(members)} คน")  # แสดงจำนวนคน
    with col2:
        st.subheader("ยอดค้างชำระรวม")
        total_debt = sum([e[2] for e in expenses])  # คำนวณผลรวมราคา
        st.info(f"{total_debt:,.2f} บาท")  # แสดงยอดเงิน
    with col3:
        st.subheader("คำแนะนำ")
        if len(members) >= 4:
            st.info("สมาชิกครบแล้ว พร้อมสำหรับการสุ่มจับคู่แล้ว!")
        else:
            st.info("ยังไม่มีข้อมูลสมาชิก")
    st.markdown("---")
    
    st.subheader("📋 รายละเอียดสมาชิกทั้งหมด")
    if members:
        df_display = pd.DataFrame(members, columns=["ชื่อ", "เลเวล", "เบอร์โทร"])  # แปลงเป็น DataFrame
        df_display['ระดับ'] = df_display['เลเวล'].map(db.level_names)  # แปลงตัวเลขเลเวลเป็นชื่อตัวอักษร
        st.dataframe(df_display[['ชื่อ', 'ระดับ', 'เบอร์โทร']], hide_index=True, use_container_width=True)  # แสดงตาราง
    else:
        st.info("ยังไม่มีข้อมูลสมาชิกในระบบ")

elif choice == "👤 จัดการสมาชิก":
    st.subheader("👤 จัดการสมาชิก")
    st.markdown("---")
    tab1, tab2, tab3 = st.tabs(["➕ เพิ่มสมาชิก", "📝 แก้ไขสมาชิก", "🗑️ ลบสมาชิก"])  # สร้างแถบย่อย
    
    with tab1:
        with st.form("add_member_form", clear_on_submit=True):  # ฟอร์มเพิ่มสมาชิก
            st.subheader("เพิ่มสมาชิกใหม่")
            name = st.text_input("ชื่อ-นามสกุล")
            phone = st.text_input("เบอร์โทรศัพท์ (10 หลัก)", max_chars=10)
            lv = st.radio("ระดับความเก่ง", options=[1, 2, 3, 4, 5, 6, 7], format_func=lambda x: f"ระดับ {db.level_names[x]}", horizontal=True)
            submit = st.form_submit_button("บันทึกข้อมูล")  # ปุ่มบันทึกในฟอร์ม
            
            if submit:
                if not name or not phone:
                    st.warning("กรุณากรอกข้อมูลให้ครบถ้วน")
                elif not (phone.isdigit() and len(phone) == 10):
                    st.error("❌ เบอร์โทรศัพท์ต้องเป็นตัวเลข 10 หลักเท่านั้น")
                else:
                    try:
                        db.cursor.execute("INSERT INTO members (name, level, phone) VALUES (?, ?, ?)", (name, lv, phone))  # บันทึกข้อมูล
                        db.conn.commit()
                        st.success(f"✅ เพิ่มคุณ {name} เรียบร้อย!")
                        st.balloons()  # แสดงเอฟเฟกต์ลูกโป่ง
                    except sqlite3.IntegrityError as e:  # ดักจับข้อผิดพลาดกรณีข้อมูลซ้ำ
                        err = str(e)
                        if "members.name" in err: st.error("⚠️ ชื่อนี้มีอยู่ในระบบแล้ว")
                        elif "members.phone" in err: st.error("⚠️ เบอร์โทรศัพท์นี้ถูกใช้งานแล้ว")
                        else: st.error("⚠️ เกิดข้อผิดพลาดในการบันทึก")

    with tab2:
        st.subheader("📝 ตารางจัดการข้อมูลสมาชิก")
        all_m = db.get_all_members()
        if all_m:
            st.markdown("---")
            head_col1, head_col2, head_col3, head_col4 = st.columns([1, 1, 1, 1])  # สร้างหัวตาราง
            head_col1.write("**ชื่อ-นามสกุล**")
            head_col2.write("**ระดับ**")
            head_col3.write("**เบอร์โทรศัพท์**")
            for m in all_m:  # วนลูปแสดงข้อมูลสมาชิกทีละแถว
                name, lv, phone = m
                c1, c2, c3, c4 = st.columns([1, 1, 1, 1])
                c1.write(name)
                c2.write(db.level_names.get(lv))
                c3.write(phone)
                if c4.button("✏️", key=f"edit_{name}"):  # ปุ่มแก้ไข
                    edit_member_dialog(name, lv, phone)  # เรียกใช้หน้าต่างแก้ไข
        else:
            st.info("ยังไม่มีข้อมูลสมาชิก")

    with tab3:
            st.subheader("🗑️ ลบข้อมูลสมาชิก")
            all_m = db.get_all_members()
            if all_m:
                st.markdown("---")
                h1, h2, h3, h4 = st.columns([1, 1, 1, 1])
                h1.write("**ชื่อ-นามสกุล**")
                h2.write("**ระดับ**")
                h3.write("**เบอร์โทรศัพท์**")
                for m in all_m:
                    name, lv, phone = m
                    c1, c2, c3, c4 = st.columns([1, 1, 1, 1])
                    c1.write(name)
                    c2.write(db.level_names.get(lv))
                    c3.write(phone)
                    if c4.button("🗑️", key=f"del_{name}"):  # ปุ่มลบ
                        delete_confirm_dialog(name)  # เรียกใช้หน้าต่างยืนยันการลบ
            else:
                st.info("ไม่มีสมาชิกในระบบให้ลบ")

elif choice == "💰 จัดการค่าใช้จ่าย":
    st.subheader("💰 จัดการค่าใช้จ่าย")
    st.markdown("---")
    tab1, tab2 = st.tabs([ "➕ เพิ่มบิลใหม่", "💸 รายการค้างชำระ"])
    
    with tab1:
        with st.form("add_expense_form", clear_on_submit=True):
            members_list = [m[0] for m in db.get_all_members()]  # ดึงรายชื่อมาทำ Dropdown
            if members_list:
                m_name = st.selectbox("เลือกสมาชิก", members_list)
                item = st.text_input("รายการ")
                price = st.number_input("ยอดเงิน (บาท)", min_value=0.0, step=10.0)
                submit = st.form_submit_button("บันทึกบิล")
                if submit:
                    db.cursor.execute("INSERT INTO expenses (member_name, item, price) VALUES (?, ?, ?)", (m_name, item, price))  # บันทึกบิล
                    db.conn.commit()
                    st.success("บันทึกข้อมูลเรียบร้อย!")
            else:
                st.info("กรุณาเพิ่มสมาชิกในระบบก่อน")
                st.form_submit_button("บันทึกบิล", disabled=True)

    with tab2:
        st.subheader("รายการที่ยังไม่ได้จ่าย")
        expenses = db.get_all_expenses()
        if expenses:
            cols = [2, 3, 2, 1] 
            h1, h2, h3, h4 = st.columns(cols)
            h1.write("**ชื่อสมาชิก**")
            h2.write("**รายการ**")
            h3.write("**ยอดเงิน**")
            h4.write("**เคลียร์**")
            st.divider()
            for ex in expenses:
                member_name, item, price = ex
                c1, c2, c3, c4 = st.columns(cols)
                c1.write(member_name)
                c2.write(item)
                c3.write(f"{price:,.2f}")
                if c4.button("🗑️", key=f"pay_{member_name}_{item}_{price}"):  # ปุ่มลบหนี้ (เมื่อจ่ายแล้ว)
                    db.cursor.execute("DELETE FROM expenses WHERE member_name = ? AND item = ? AND price = ?", (member_name, item, price))
                    db.conn.commit()
                    st.rerun()
        else:
            st.success("ไม่มียอดค้างชำระในขณะนี้")

elif choice == "🎲 สุ่มจับคู่":
    st.header("🎲 สุ่มจับคู่")
    st.markdown("---")
    col_a, col_b = st.columns([1, 1])
    with col_a:
        match_mode = st.radio("เลือกโหมดการเล่น", ["เดี่ยว (1 VS 1)", "คู่ (2 VS 2)"], horizontal=True)
    with col_b:
        lv_to_match = st.selectbox("เลือกระดับที่ต้องการสุ่ม", [1,2,3,4,5,6,7], format_func=lambda x: db.level_names[x])
    
    if st.button("🚀 เริ่มสุ่มคู่", use_container_width=True):
        st.markdown("---")
        db.cursor.execute("SELECT name FROM members WHERE level = ?", (lv_to_match,))  # ดึงสมาชิกตามเลเวลที่เลือก
        pool = [row[0] for row in db.cursor.fetchall()]  # เก็บรายชื่อใส่ List
        required_people = 2 if match_mode == "เดี่ยว (1 VS 1)" else 4  # จำนวนคนที่ต้องใช้ต่อสนาม
        
        if len(pool) < required_people:
            st.error(f"สมาชิกไม่เพียงพอ! ต้องการอย่างน้อย {required_people} คน")
        else:
            random.shuffle(pool)  # สลับรายชื่อแบบสุ่ม
            st.balloons()
            st.subheader("ผลการสุ่มคู่")
            for i in range(0, len(pool) - (len(pool) % required_people), required_people):  # วนลูปจัดสนาม
                with st.container(border=True):
                    st.markdown(f"### 🏟️ สนามที่ {i // required_people + 1}")
                    if match_mode == "เดี่ยว (1 VS 1)":
                        c1, c2, c3 = st.columns([2, 1.5, 2])
                        c1.metric(label="ทีม A", value=pool[i])
                        c2.subheader("VS")
                        c3.metric(label="ทีม B", value=pool[i+1])
                    else:
                        cola, colvs, colb = st.columns([2, 1.5, 2])
                        with cola: st.markdown(f"**ทีม A**\n### {pool[i]}\n### {pool[i+1]}")
                        with colvs: st.markdown("<br><br><h2>VS</h2>", unsafe_allow_html=True)
                        with colb: st.markdown(f"**ทีม B**\n### {pool[i+2]}\n### {pool[i+3]}")

            if len(pool) % required_people != 0:  # ถ้ามีคนเหลือเศษ
                st.markdown("---")
                leftovers = pool[-(len(pool) % required_people):]
                st.markdown("### รายชื่อผู้รอสลับ")
                with st.container(border=True):
                    st.subheader(" , ".join(leftovers))

elif choice == "💾 สำรองข้อมูล":
    st.header("💾 สำรองและส่งออกข้อมูล")
    st.markdown("---")
    members = db.get_all_members()
    expenses = db.get_all_expenses()
    col_stat1, col_stat2 = st.columns(2)
    col_stat1.metric("สมาชิกทั้งหมด", f"{len(members)} รายการ")
    col_stat2.metric("หนี้สินทั้งหมด", f"{len(expenses)} รายการ")
    st.markdown("<br>", unsafe_allow_html=True)

    col_left, col_right = st.columns(2)
    with col_left:
        with st.container(border=True):
            st.subheader("👥 ข้อมูลสมาชิก")
            if members:
                df_m = pd.DataFrame(members, columns=["ชื่อ-นามสกุล", "ระดับเลข", "เบอร์โทรศัพท์"])
                csv_m = df_m.to_csv(index=False).encode('utf-8-sig')  # แปลงเป็น CSV (utf-8-sig รองรับภาษาไทยใน Excel)
                st.download_button("📥 ดาวน์โหลดรายชื่อสมาชิก", data=csv_m, file_name='member_list.csv', mime='text/csv', use_container_width=True)
            else: st.info("ไม่มีข้อมูล")

    with col_right:
        with st.container(border=True):
            st.subheader("💰 รายการทางบัญชี")
            if expenses:
                df_e = pd.DataFrame(expenses, columns=["ชื่อสมาชิก", "รายการ", "ยอดเงิน"])
                csv_e = df_e.to_csv(index=False).encode('utf-8-sig')  # แปลงเป็น CSV
                st.download_button("📥 ดาวน์โหลดรายการบัญชี", data=csv_e, file_name='expense_report.csv', mime='text/csv', use_container_width=True)
            else: st.info("ไม่มีข้อมูล")
    st.markdown("---")
    st.caption("💡 แนะนำ: ไฟล์ CSV สามารถเปิดได้ใน Excel หรือ Google Sheets")