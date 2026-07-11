import streamlit as st

# إعدادات الصفحة الأساسية
st.set_page_config(page_title="تطبيق الكيمياء الذكي", page_icon="🧪", layout="centered")

# حقن تنسيقات CSS مخصصة لتحويل التطبيق بالكامل إلى اللون الأزرق الغامق الجذاب
st.markdown("""
    <style>
    /* 1️⃣ تغيير خلفية التطبيق بالكامل إلى الأزرق الغامق الفاخر */
    [data-testid="stAppViewContainer"] {
        background-color: #0A192F !important;
    }
    
    /* جعل الهيدر العلوي شفافاً ليتناسق مع الخلفية */
    [data-testid="stHeader"] {
        background-color: rgba(0,0,0,0) !important;
    }

    /* 2️⃣ تلوين العناوين والنصوص باللون الأبيض لضمان وضوحها الشديد */
    h1, h2, h3, h4, h5, h6, span {
        color: #F8FAFC !important;
    }
    
    /* تلوين نصوص الأسئلة والاختيارات داخل الـ Radio Buttons */
    div[data-testid="stMarkdownContainer"] p {
        color: #F8FAFC !important;
        font-size: 17px;
    }
    
    /* 3️⃣ تصميم صندوق الترحيب بلمسة زرقاء تقنية مضيئة */
    .welcome-box {
        border: 3px solid #00b4d8; 
        border-radius: 16px; 
        background-color: #172A45; 
        padding: 35px 20px; 
        text-align: center; 
        margin: 25px auto;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.5);
    }
    .welcome-title {
        color: #00b4d8 !important; font-size: 32px; font-weight: bold; margin: 0;
    }
    .credits {
        color: #4ade80; text-align: center; font-size: 20px; font-weight: bold; margin-bottom: 35px; direction: rtl;
    }
    
    /* تحسين مظهر الأزرار لتكون بارزة وجذابة */
    .stButton>button {
        border-radius: 8px !important;
        font-weight: bold !important;
        font-size: 16px !important;
    }
    </style>
""", unsafe_allow_html=True)

# إدارة حالة التطبيق (Session State)
if "started" not in st.session_state:
    st.session_state.started = False
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "answered" not in st.session_state:
    st.session_state.answered = False
if "user_choice" not in st.session_state:
    st.session_state.user_choice = None

# بنك الأسئلة الوزارية 
questions = [
    {
        "question": "التوزيع الإلكتروني الصحيح لعنصر الكروم Cr²⁴ هو:",
        "options": ["[Ar] 3d⁵ 4s¹", "[Ar] 3d⁴ 4s²", "[Ar] 3d³ 4s²", "[Ar] 3d⁶ 4s⁰"],
        "answer": "[Ar] 3d⁵ 4s¹"
    },
    {
        "question": "أي من العناصر التالية يعتبر من العناصر الانتقالية في الجدول الدوري؟",
        "options": ["الصوديوم (Na)", "الحديد (Fe)", "الكالسيوم (Ca)", "الألومنيوم (Al)"],
        "answer": "الحديد (Fe)"
    },
    {
        "question": "ما هو الرقم الهيدروجيني (pH) للمحلول المتعادل تماماً عند درجة حرارة 25°C؟",
        "options": ["0", "7", "14", "1"],
        "answer": "7"
    }
]

# 1️⃣ الواجهة الترحيبية الاحترافية باللون الجديد
if not st.session_state.started:
    st.markdown('<div class="welcome-box"><h1 class="welcome-title">الدخول الى الاسئله</h1></div>', unsafe_allow_html=True)
    st.markdown('<div class="credits">انتاج وتصميم وبرمجه المبرمج عبدالرحمن الاسدي</div>', unsafe_allow_html=True)
    
    if st.button("اضغط هنا لبدء الاختبار 🚀", use_container_width=True, type="primary"):
        st.session_state.started = True
        st.rerun()

# 2️⃣ واجهة الأسئلة والاختبار التفاعلي المطور
else:
    st.title("🎓 بنك الأسئلة الوزارية - كيمياء")
    total_q = len(questions)
    
    if st.session_state.current_question < total_q:
        q_idx = st.session_state.current_question
        q = questions[q_idx]
        
        st.markdown(f"### 🧪 السؤال {q_idx + 1} من {total_q}")
        st.info(q["question"])
        
        # الحالة الأولى: الطالب لم يؤكد إجابته بعد
        if not st.session_state.answered:
            choice = st.radio("اختر الإجابة الصحيحة من الخيارات التالية:", q["options"], index=None, key=f"q_{q_idx}")
            
            if st.button("✔ تأكيد الإجابة", use_container_width=True, type="primary"):
                if choice is None:
                    st.warning("⚠️ الرجاء اختيار إجابة أولاً قبل التأكيد!")
                else:
                    st.session_state.answered = True
                    st.session_state.user_choice = choice
                    if choice == q["answer"]:
                        st.session_state.score += 1
                    st.rerun()
                    
        # الحالة الثانية: تم تأكيد الإجابة، نعرض النتيجة بوضوح مع قفل الاختيارات
        else:
            user_choice_index = q["options"].index(st.session_state.user_choice)
            st.radio("إجابتك المختارة والمقفلة:", q["options"], index=user_choice_index, disabled=True, key=f"q_done_{q_idx}")
            
            # إظهار التقييم الملون الفوري
            if st.session_state.user_choice == q["answer"]:
                st.success("✅ إجابة صحيحة! أحسنت وممتاز 🎉")
            else:
                st.error(f"❌ إجابة خاطئة! الإجابة الصحيحة هي: {q['answer']}")
            
            # زر انتقال اختياري ومريح للسؤال التالي
            if st.button("السؤال التالي ➡️", use_container_width=True):
                st.session_state.current_question += 1
                st.session_state.answered = False
                st.session_state.user_choice = None
                st.rerun()
            
    else:
        # 3️⃣ واجهة النتيجة النهائية عند انتهاء الأسئلة
        st.balloons()
        st.markdown('<div class="welcome-box"><h2 class="welcome-title">🎉 تهانينا! لقد أتممت الاختبار بنجاح</h2></div>', unsafe_allow_html=True)
        
        score = st.session_state.score
        percentage = (score / total_q) * 100
        
        st.metric(label="درجتك النهائية هي:", value=f"{score} من {total_q}", delta=f"{percentage:.1f}%")
        
        if percentage >= 50:
            st.success("أداء ممتاز ورائع! استمر في التقدم العلمي 🚀")
        else:
            st.warning("تحتاج إلى مراجعة بعض المفاهيم، يمكنك المحاولة مجدداً بالضغط على الزر أدناه!")
            
        if st.button("إعادة الاختبار مجدداً 🔄", use_container_width=True):
            st.session_state.started = False
            st.session_state.current_question = 0
            st.session_state.score = 0
            st.session_state.answered = False
            st.session_state.user_choice = None
            st.rerun()
