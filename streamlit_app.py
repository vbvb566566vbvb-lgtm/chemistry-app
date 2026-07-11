import streamlit as st

# إعدادات الصفحة الأساسية لتناسب شاشات الهواتف والكمبيوتر
st.set_page_config(page_title="تطبيق الكيمياء الذكي", page_icon="🧪", layout="centered")

# تنسيقات مخصصة (CSS) لتصميم المستطيل الأزرق وحقوقك باللون الأخضر
st.markdown("""
    <style>
    .welcome-box {
        border: 3px solid #4A90E2; 
        border-radius: 12px; 
        background-color: #ffffff; 
        padding: 30px 20px; 
        text-align: center; 
        margin: 20px auto;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.05);
    }
    .welcome-title {
        color: #2C3E50; font-size: 28px; font-weight: bold; margin: 0;
    }
    .credits {
        color: #27AE60; text-align: center; font-size: 18px; font-weight: bold; margin-bottom: 30px; direction: rtl;
    }
    </style>
""", unsafe_allow_html=True)

# إدارة حالة التطبيق (Session State) لحفظ تقدم الطالب ومنع إعادة تعيين الأسئلة
if "started" not in st.session_state:
    st.session_state.started = False
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
    st.session_state.score = 0

# بنك الأسئلة الوزارية (يمكنك تعديل الأسئلة والاختيارات والإجابات في أي وقت هنا)
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

# 1️⃣ الواجهة الترحيبية الاحترافية الأولى
if not st.session_state.started:
    st.markdown('<div class="welcome-box"><h1 class="welcome-title">الدخول الى الاسئله</h1></div>', unsafe_allow_html=True)
    st.markdown('<div class="credits">انتاج وتصميم وبرمجه المبرمج عبدالرحمن الاسدي</div>', unsafe_allow_html=True)
    
    if st.button("اضغط هنا لبدء الاختبار 🚀", use_container_width=True, type="primary"):
        st.session_state.started = True
        st.rerun()

# 2️⃣ واجهة الأسئلة والاختبار التفاعلي
else:
    st.title("🎓 بنك الأسئلة الوزارية - كيمياء")
    total_q = len(questions)
    
    if st.session_state.current_question < total_q:
        q_idx = st.session_state.current_question
        q = questions[q_idx]
        
        st.markdown(f"### 🧪 السؤال {q_idx + 1} من {total_q}")
        st.info(q["question"])
        
        # عرض الخيارات للطالب
        choice = st.radio("اختر الإجابة الصحيحة من الخيارات التالية:", q["options"], key=f"q_{q_idx}")
        
        # زر تأكيد الإجابة للانتقال للسؤال التالي
        if st.button("تأكيد الإجابة والانتقال للسؤال التالي ➡️", use_container_width=True, type="primary"):
            if choice == q["answer"]:
                st.session_state.score += 1
                st.success("إجابة صحيحة! أحسنت وممتاز 🎉")
            else:
                st.error(f"إجابة خاطئة. الإجابة الصحيحة هي: {q['answer']}")
                
            st.session_state.current_question += 1
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
            
        # زر لإعادة الاختبار من جديد
        if st.button("إعادة الاختبار مجدداً 🔄", use_container_width=True):
            st.session_state.started = False
            st.session_state.current_question = 0
            st.session_state.score = 0
            st.rerun()
          
