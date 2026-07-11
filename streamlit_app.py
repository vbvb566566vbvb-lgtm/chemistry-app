import streamlit as st

# إعدادات الصفحة الأساسية لتناسب شاشات الهواتف والكمبيوتر
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

# بنك الأسئلة المأخوذة مباشرة من أوراق العمل الخاصة بك (الباب الأول: العناصر الانتقالية)
questions = [
    {
        "question": "عناصر يتتابع فيها امتلاء المستوى الفرعي 3d وتبدأ بعنصر السكانديوم وتنتهي بعنصر الخارصين هي:",
        "options": ["السلسلة الانتقالية الأولى", "السلسلة الانتقالية الثانية", "السلسلة الانتقالية الثالثة", "العناصر الممثلة"],
        "answer": "السلسلة الانتقالية الأولى"
    },
    {
        "question": "العنصر الانتقالي الذي يتميز بخفته وصلابته الشديدة وتصنع منه طائرات الميج المقاتلة عند إضافته للألومنيوم هو:",
        "options": ["السكانديوم (Sc)", "التيتانيوم (Ti)", "الفاناديوم (V)", "المنجنيز (Mn)"],
        "answer": "السكانديوم (Sc)"
    },
    {
        "question": "يستخدم هذا العنصر الانتقالي في عمليات زراعة الأسنان والمفاصل الصناعية لأن الجسم لا يلفظه ولا يسبب أي تسمم:",
        "options": ["الحديد (Fe)", "النيكل (Ni)", "التيتانيوم (Ti)", "الكروم (Cr)"],
        "answer": "التيتانيوم (Ti)"
    },
    {
        "question": "المركب الذي يستخدم كعامل حفاز في صناعة المغناطيسيات فائقة التوصيل وصبغة في صناعة السيراميك والزجاج هو:",
        "options": ["خامس أكسيد الفاناديوم (V₂O₅)", "ثاني أكسيد المنجنيز (MnO₂)", "أكسيد الكروم (Cr₂O₃)", "كبريتات النحاس (CuSO₄)"],
        "answer": "خامس أكسيد الفاناديوم (V₂O₅)"
    },
    {
        "question": "يقاوم عنصر الكروم (Cr) فعل العوامل الجوية بسبب تآكله السريع أم لسبب آخر؟",
        "options": ["لأنه عنصر غير نشط كيميائياً", "لتكون طبقة من الأكسيد غير مسامية على سطحه", "لأنه يتفاعل مع الهيدروجين", "بسبب شدة صلابته ومقاومته للخدش"],
        "answer": "لتكون طبقة من الأكسيد غير مسامية على سطحه"
    },
    {
        "question": "تستخدم سبيكة (الحديد مع المنجنيز) في صناعة خطوط السكك الحديدية لأنها تمتاز بأنها:",
        "options": ["أخف من الألومنيوم", "مقاومة للكهرباء العالية", "أصلب من الصلب نفسه", "ذات مظهر برّاق وجذاب"],
        "answer": "أصلب من الصلب نفسه"
    },
    {
        "question": "تستخدم طريقة (فيشر - تروبش) لتحويل الغاز المائي (خليط H₂ و CO) إلى وقود سائل باستخدام عامل حفاز هو:",
        "options": ["البلاتين (Pt)", "النيكل المجزأ (Ni)", "الحديد المجزأ (Fe)", "النحاس (Cu)"],
        "answer": "الحديد المجزأ (Fe)"
    },
    {
        "question": "النظير المشع لعنصر الكوبالت والذي يصدر أشعة جاما ذات القدرة العالية على النفاذ وتستخدم في حفظ الأغذية هو:",
        "options": ["كوبالت 50", "كوبالت 60", "كوبالت 70", "كوبالت 58"],
        "answer": "كوبالت 60"
    },
    {
        "question": "تستخدم سبائك (النيكل - كروم) بشكل أساسي في صناعة:",
        "options": ["عبوات المشروبات الغازية", "ملفات التسخين والأفران الكهربائية", "هياكل الطائرات الفضائية", "مغناطيسيات فائقة التوصيل"],
        "answer": "ملفات التسخين والأفران الكهربائية"
    },
    {
        "question": "محلول (فهيدنج) الذي يتحول من اللون الأزرق إلى البرتقالي للكشف عن سكر الجلوكوز يعتبر من مركبات عنصر:",
        "options": ["الحديد", "الخارصين", "الكروم", "النحاس"],
        "answer": "النحاس"
    },
    {
        "question": "جميع عناصر السلسلة الانتقالية الأولى تعطي حالة التأكسد (+2) عند فقد إلكترونات 4s ما عدا عنصر:",
        "options": ["الحديد (Fe)", "السكانديوم (Sc)", "المنجنيز (Mn)", "الخارصين (Zn)"],
        "answer": "السكانديوم (Sc)"
    },
    {
        "question": "العنصر الانتقالي الذي يمتلك أعلى حالة تأكسد في السلسلة الانتقالية الأولى وتصل إلى (+7) هو:",
        "options": ["الحديد (Fe)", "الكروم (Cr)", "المنجنيز (Mn)", "الفاناديوم (V)"],
        "answer": "المنجنيز (Mn)"
    },
    {
        "question": "يعتبر عنصر الخارصين (Zn³⁰) عنصراً غير انتقالي وذلك لأن:",
        "options": ["المستوى الفرعي 3d ممتلئ تماماً في الحالة الذرية وحالة التأكسد الوحيدة له (+2)", "لا يتفاعل مع الأحماض المخففة", "ليس له استخدامات اقتصادية في الصناعة", "حالة تأكسده تصل إلى (+4) "],
        "answer": "المستوى الفرعي 3d ممتلئ تماماً في الحالة الذرية وحالة التأكسد الوحيدة له (+2)"
    },
    {
        "question": "تعتبر عناصر العملة (النحاس والفضة والذهب) عناصر انتقالية لأن المستويات الفرعية d تكون:",
        "options": ["فارغة تماماً من الإلكترونات", "ممتلئة في جميع الحالات", "مشغولة بالإلكترونات وليست ممتلئة في حالتي التأكسد (+2, +3)", "تحتوي على إلكترونات مزدوجة فقط"],
        "answer": "مشغولة بالإلكترونات وليست ممتلئة في حالتي التأكسد (+2, +3)"
    },
    {
        "question": "المادة التي تنجذب نحو المجال المغناطيسي الخارجي نتيجة لوجود إلكترونات مفردة في مستواها الفرعي d تسمى مادة:",
        "options": ["دايامغناطيسية", "بارامغناطيسية", "ممثلة", "خاملة كيميائياً"],
        "answer": "بارامغناطيسية"
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
