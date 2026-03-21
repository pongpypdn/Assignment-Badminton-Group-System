import streamlit as st
import sqlite3
import random
import pandas as pd

@st.dialog("แก้ไขข้อมูลสมาชิก")
def edit_member_dialog(name, lv, phone):
    st.write(f"กำลังแก้ไขข้อมูลคุณ: **{name}**")
    with st.expander("✏️ แก้ไขชื่อ"):
        new_name = st.text_input("ชื่อใหม่", value=name)
        if st.button("บันทึกชื่อ"):
            db.cursor.execute("UPDATE members SET name = ? WHERE name = ?", (new_name, name))
            db.cursor.execute("UPDATE expenses SET member_name = ? WHERE member_name = ?", (new_name, name))
            db.conn.commit()
            st.rerun()

    with st.expander("📞 แก้ไขเบอร์โทร"):
        new_phone = st.text_input("เบอร์ใหม่", value=phone, max_chars=10)
        if st.button("บันทึกเบอร์"):
            db.cursor.execute("UPDATE members SET phone = ? WHERE name = ?", (new_phone, name))
            db.conn.commit()
            st.rerun()

    with st.expander("🏆 แก้ไขระดับ"): 
        new_lv = st.radio("เลือกระดับใหม่", ["BG", "N-", "N", "NS", "S", "P-", "P" ], index=lv-1, horizontal=True)  
        if st.button("บันทึกระดับ"):  
            lv_val = ["BG", "N-", "N", "NS", "S", "P-", "P"].index(new_lv) + 1
            db.cursor.execute("UPDATE members SET level = ? WHERE name = ?", (lv_val, name))  
            db.conn.commit() 
            st.rerun()  

@st.dialog("⚠️ ยืนยันการลบสมาชิก")
def delete_confirm_dialog(name):
    st.write(f"คุณต้องการลบข้อมูลของคุณ **{name}** ใช่หรือไม่ ?")
    st.write("การลบจะไม่สามารถกู้คืนได้ และจะลบข้อมูลที่เกี่ยวข้องทั้งหมดด้วย")
    
    col1, col2 = st.columns(2)
    if col1.button("ยืนยันการลบ", type="primary"):
        db.cursor.execute("DELETE FROM members WHERE name = ?", (name,))
        db.cursor.execute("DELETE FROM expenses WHERE member_name = ?", (name,))
        db.conn.commit()
        st.success("ลบข้อมูลเรียบร้อย")
        st.rerun() 
    if col2.button("ยกเลิก"):
        st.rerun()

st.set_page_config(page_title="BADMINTON GROUP SYSTEM", page_icon="🏸", layout="wide")

def set_custom_font():
    st.markdown("""
    <style>
    /* นำเข้าฟอนต์จาก Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500;600&display=swap');

    /* บังคับใช้ฟอนต์กับทุกส่วนของหน้าเว็บ */
    html, body, [class*="css"], .stApp, .stButton, .stTextInput, .stMarkdown, p, h1, h2, h3, h4, h5, h6 {
        font-family: 'Kanit', sans-serif !important;
    }
    </style>
    """, unsafe_allow_html=True)

# เรียกใช้ฟังก์ชันนี้บรรทัดแรกหลัง import
set_custom_font()

class BadmintonWebSystem:
    def __init__(self, db_name="badminton_club.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.level_names = {7: "P",6: "P-",5: "S", 4: "NS", 3: "N", 2: "N-", 1: "BG"}
        self._create_tables()

    def _create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS members (
                name TEXT PRIMARY KEY, 
                level INTEGER, 
                phone TEXT UNIQUE
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                member_name TEXT,
                item TEXT,
                price REAL,
                FOREIGN KEY (member_name) REFERENCES members(name)
            )
        ''')
        self.conn.commit()

    def get_all_members(self):
        self.cursor.execute("SELECT name, level, phone FROM members")
        return self.cursor.fetchall()

    def get_all_expenses(self):
        self.cursor.execute("SELECT member_name, item, price FROM expenses")
        return self.cursor.fetchall()

db = BadmintonWebSystem()

menu_items = ["📊 ภาพรวมระบบ", "👤 จัดการสมาชิก", "💰 จัดการค่าใช้จ่าย", "🎲 สุ่มจับคู่", "💾 สำรองข้อมูล"]

if 'current_page' not in st.session_state:
    st.session_state.current_page = menu_items[0]

with st.sidebar:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("assets/badminton_kmutnb.png", width=200)
    st.markdown("<h2 style='text-align: center;'>BADMINTON GROUP SYSTEM</h2>", unsafe_allow_html=True)
    st.caption("<h5 style='text-align: center;'>PROBLEM SOLVING PROJECT</h5>", unsafe_allow_html=True)
    st.markdown("---")
    st.write("**เมนูควบคุม**")

    for item in menu_items:
        if st.button(item, use_container_width=True, type="secondary"):
            st.session_state.current_page = item
            st.rerun()
    st.markdown("---")
    st.caption("<h5 style='text-align: center;'>BADMINTON KMUTNB PRACHINBURI</h5>", unsafe_allow_html=True)
    choice = st.session_state.current_page

if choice == "📊 ภาพรวมระบบ":
    st.subheader("📊 ภาพรวมระบบ")
    st.markdown("---")
    members = db.get_all_members()
    expenses = db.get_all_expenses()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("จำนวนสมาชิกทั้งหมด")
        st.info(f"{len(members)} คน")
    with col2:
        st.subheader("ยอดค้างชำระรวม")
        total_debt = sum([e[2] for e in expenses])
        st.info(f"{total_debt:,.2f} บาท")
    with col3:
        st.subheader("คำแนะนำ")
        if len(members) >= 4:
            st.info("สมาชิกครบแล้ว พร้อมสำหรับการสุ่มจับคู่แล้ว!")
        else:
            st.info("ยังไม่มีข้อมูลสมาชิก")
    st.markdown("---")
    
    st.subheader("📋 รายละเอียดสมาชิกทั้งหมด")
    if members:
        df_display = pd.DataFrame(members, columns=["ชื่อ", "เลเวล", "เบอร์โทร"])
        df_display['ระดับ'] = df_display['เลเวล'].map(db.level_names)
        st.dataframe(df_display[['ชื่อ', 'ระดับ', 'เบอร์โทร']], hide_index=True, use_container_width=True)
    else:
        st.info("ยังไม่มีข้อมูลสมาชิกในระบบ")

elif choice == "👤 จัดการสมาชิก":
    st.subheader("👤 จัดการสมาชิก")
    st.markdown("---")
    tab1, tab2, tab3 = st.tabs(["➕ เพิ่มสมาชิก", "📝 แก้ไขสมาชิก", "🗑️ ลบสมาชิก"])
    
    with tab1:
        with st.form("add_member_form", clear_on_submit=True):
            st.subheader("เพิ่มสมาชิกใหม่")
            name = st.text_input("ชื่อ-นามสกุล")
            phone = st.text_input("เบอร์โทรศัพท์ (10 หลัก)", max_chars=10)

            lv = st.radio(
                "ระดับความเก่ง", 
                options=[1, 2, 3, 4, 5, 6, 7], 
                format_func=lambda x: f"ระดับ {db.level_names[x]}",
                horizontal=True
            )
            
            submit = st.form_submit_button("บันทึกข้อมูล")
            
            if submit:
                if not name or not phone:
                    st.warning("กรุณากรอกข้อมูลให้ครบถ้วน")
                elif not (phone.isdigit() and len(phone) == 10):
                    st.error("❌ เบอร์โทรศัพท์ต้องเป็นตัวเลข 10 หลักเท่านั้น")
                else:
                    try:
                        db.cursor.execute("INSERT INTO members (name, level, phone) VALUES (?, ?, ?)", (name, lv, phone))
                        db.conn.commit()
                        st.success(f"✅ เพิ่มคุณ {name} เรียบร้อย!")
                        st.balloons()
                    except sqlite3.IntegrityError as e:
                        err = str(e)
                        if "members.name" in err:
                            st.error("⚠️ ชื่อนี้มีอยู่ในระบบแล้ว")
                        elif "members.phone" in err:
                            st.error("⚠️ เบอร์โทรศัพท์นี้ถูกใช้งานแล้วโดยสมาชิกคนอื่น")
                        else:
                            st.error("⚠️ เกิดข้อผิดพลาดในการบันทึกข้อมูล")

    with tab2:
        st.subheader("📝 ตารางจัดการข้อมูลสมาชิก")
        all_m = db.get_all_members()
        
        if all_m:
            st.markdown("---")
            cols = [1, 1, 1, 1]
            head_col1, head_col2, head_col3, head_col4 = st.columns([1, 1, 1, 1])
            with head_col1: st.write("**ชื่อ-นามสกุล**")
            with head_col2: st.write("**ระดับ**")
            with head_col3: st.write("**เบอร์โทรศัพท์**")
            
            for m in all_m:
                name, lv, phone = m
                c1, c2, c3, c4 = st.columns(cols)
                c1.write(name)
                c2.write(db.level_names.get(lv))
                c3.write(phone)
                if c4.button("✏️", key=f"edit_{name}"):
                    edit_member_dialog(name, lv, phone)
        else:
            st.info("ยังไม่มีข้อมูลสมาชิก")

    with tab3:
            st.subheader("🗑️ ลบข้อมูลสมาชิก")
            all_m = db.get_all_members()
            
            if all_m:
                st.markdown("---")
                cols = [1, 1, 1, 1]
                h1, h2, h3, h4 = st.columns(cols)
                h1.write("**ชื่อ-นามสกุล**")
                h2.write("**ระดับ**")
                h3.write("**เบอร์โทรศัพท์**")
                
                
                for m in all_m:
                    name, lv, phone = m
                    c1, c2, c3, c4 = st.columns(cols)
                    c1.write(name)
                    c2.write(db.level_names.get(lv))
                    c3.write(phone)
                    
                    if c4.button("🗑️", key=f"del_{name}"):
                        delete_confirm_dialog(name)
            else:
                st.info("ไม่มีสมาชิกในระบบให้ลบ")

elif choice == "💰 จัดการค่าใช้จ่าย":
    st.subheader("💰 จัดการค่าใช้จ่าย")
    st.markdown("---")
    tab1, tab2 = st.tabs([ "➕ เพิ่มบิลใหม่", "💸 รายการค้างชำระ"])

    with tab1:
        with st.form("add_expense_form", clear_on_submit=True):
            members_list = [m[0] for m in db.get_all_members()]

            if members_list:
                m_name = st.selectbox("เลือกสมาชิก", members_list)
                item = st.text_input("รายการ")
                price = st.number_input("ยอดเงิน (บาท)", min_value=0.0, step=10.0)

                submit = st.form_submit_button("บันทึกบิล")
                
                if submit:
                    db.cursor.execute("INSERT INTO expenses (member_name, item, price) VALUES (?, ?, ?)", (m_name, item, price))
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
                
                if c4.button("🗑️", key=f"pay_{member_name}_{item}"):
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
        db.cursor.execute("SELECT name FROM members WHERE level = ?", (lv_to_match,))
        pool = [row[0] for row in db.cursor.fetchall()]
        
        required_people = 2 if match_mode == "เดี่ยว (1 VS 1)" else 4
        
        if len(pool) < required_people:
            st.error(f"สมาชิกไม่เพียงพอ! ต้องการอย่างน้อย {required_people} คน")
        else:
            random.shuffle(pool)
            st.balloons()
            
            st.subheader("ผลการสุ่มคู่")
            for i in range(0, len(pool) - (len(pool) % required_people), required_people):
                with st.container(border=True):
                    st.markdown(f"### 🏟️ สนามที่ {i // required_people + 1}")
                    if match_mode == "เดี่ยว (1 VS 1)":
                        c1, c2, c3 = st.columns([2, 1.5, 2])
                        c1.metric(label="ทีม A", value=pool[i])
                        c2.subheader("VS")
                        c3.metric(label="ทีม B", value=pool[i+1])
                    else:
                        for i in range(0, len(pool) - (len(pool) % 4), 4):
                            with st.container(border=False):

                                col_a, col_vs, col_b = st.columns([2, 1.5, 2])

                                with col_a:
                                    st.write("ทีม A")
                                    st.markdown(f"### {pool[i]}")
                                    st.markdown(f"### {pool[i+1]}")

                                with col_vs:
                                    st.markdown("<br><br>", unsafe_allow_html=True)
                                    st.header("VS")

                                with col_b:
                                    st.write("ทีม B")
                                    st.markdown(f"### {pool[i+2]}")
                                    st.markdown(f"### {pool[i+3]}")

            if len(pool) % required_people != 0:
                st.markdown("---")
                leftovers = pool[-(len(pool) % required_people):]
                st.markdown("### รายชื่อผู้รอสลับ")
                with st.container(border=True):
                    st.subheader(" , ".join(leftovers))
        st.markdown("---")
        
elif choice == "💾 สำรองข้อมูล":
    st.header("💾 สำรองและส่งออกข้อมูล")
    st.markdown("---")

    members = db.get_all_members()
    expenses = db.get_all_expenses()
    
    col_stat1, col_stat2 = st.columns(2)
    with col_stat1:
        st.metric("ข้อมูลสมาชิกที่พร้อมส่งออก", f"{len(members)} รายการ")
    with col_stat2:
        st.metric("รายการบัญชีที่พร้อมส่งออก", f"{len(expenses)} รายการ")
    st.markdown("---")
    st.markdown("<br>", unsafe_allow_html=True)

    col_left, col_right = st.columns(2)

    with col_left:
        with st.container(border=True):
            st.subheader("👥 ข้อมูลสมาชิก")
            st.write("ส่งออกรายชื่อสมาชิก ระดับฝีมือ และเบอร์โทรศัพท์ทั้งหมดเป็นไฟล์ CSV")
            if members:
                df_members = pd.DataFrame(members, columns=["ชื่อ-นามสกุล", "ระดับ", "เบอร์โทรศัพท์"])
                csv_members = df_members.to_csv(index=False).encode('utf-8-sig')
                st.download_button(
                    label="📥 ดาวน์โหลดรายชื่อสมาชิก",
                    data=csv_members,
                    file_name='member_list.csv',
                    mime='text/csv',
                    use_container_width=True
                )
            else:
                st.info("ไม่มีข้อมูลให้ดาวน์โหลด")

    with col_right:
        with st.container(border=True):
            st.subheader("💰 รายการทางบัญชี")
            st.write("ส่งออกรายการค้างชำระทั้งหมดเป็นไฟล์ CSV")
            if expenses:
                df_expenses = pd.DataFrame(expenses, columns=["ชื่อสมาชิก", "รายการ", "ยอดเงิน"])
                csv_expenses = df_expenses.to_csv(index=False).encode('utf-8-sig')
                st.download_button(
                    label="📥 ดาวน์โหลดรายการบัญชี",
                    data=csv_expenses,
                    file_name='expense_report.csv',
                    mime='text/csv',
                    use_container_width=True
                )
            else:
                st.info("ไม่มีข้อมูลให้ดาวน์โหลด")

    st.markdown("---")
    st.caption("💡 **คำแนะนำ:** ไฟล์ที่ดาวน์โหลดจะเป็นรูปแบบ `.csv` ซึ่งสามารถเปิดใช้งานได้ทันทีใน Microsoft Excel, Google Sheets")