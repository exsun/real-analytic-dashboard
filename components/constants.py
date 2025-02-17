CHABOKI_DATA=[
    { "taste": "سرعت عکس العمل", "pre-test": 93, "post-test": 61},
    { "taste": "سرعت واکنش", "pre-test": 91, "post-test": 37},
    { "taste": "تعادل پویا", "pre-test": 56, "post-test": 95},
    { "taste": "هماهنگی", "pre-test": 64, "post-test": 90},
    { "taste": "زمان واکنش", "pre-test": 119, "post-test": 94}
]

SORAT_DATA=[
    { "taste": "یک تکرار بیشینه", "pre-test": 93, "post-test": 61},
    { "taste": "سرعت واکنش", "pre-test": 91, "post-test": 37},
    { "taste": "تعادل پویا", "pre-test": 56, "post-test": 95},
    { "taste": "هماهنگی", "pre-test": 64, "post-test": 90},
    { "taste": "زمان واکنش", "pre-test": 119, "post-test": 94}
]

GHODRAT_DATA=[
    { "taste": "یک تکرار بیشینه", "pre-test": 93, "post-test": 61},
    { "taste": "۵۰ ٪", "pre-test": 91, "post-test": 37},
    { "taste": "۶۰ ٪", "pre-test": 56, "post-test": 95},
    { "taste": "۷۰ ٪", "pre-test": 64, "post-test": 90},
    { "taste": "۷۵ ٪", "pre-test": 119, "post-test": 94},
    { "taste": "۸۰ ٪", "pre-test": 45, "post-test": 85},
    { "taste": "۸۵ ٪", "pre-test": 65, "post-test": 70},
    { "taste": "۹۰ ٪", "pre-test": 45, "post-test": 96}
]

GHODRAT_SQUAT_DATA=[
    { "taste": "یک تکرار بیشینه", "pre-test": 171, "post-test": 61},
    { "taste": "۵۰ ٪", "pre-test": 190, "post-test": 37},
    { "taste": "۶۰ ٪", "pre-test": 95, "post-test": 95},
    { "taste": "۷۰ ٪", "pre-test": 114, "post-test": 90},
    { "taste": "۷۵ ٪", "pre-test": 133, "post-test": 94},
    { "taste": "۸۰ ٪", "pre-test": 143, "post-test": 85},
    { "taste": "۸۵ ٪", "pre-test": 152, "post-test": 70},
    { "taste": "۹۰ ٪", "pre-test": 161, "post-test": 96}
]

EXERCISE_OPTIONS = [
    "پرس سینه", "اسکات", "ددلیفت", "پرس سرشانه", "کلین و جرک",
    "اسنچ", "بارفیکس", "شنا", "پشت بازو", "جلوبازو",
    "لانگز", "پرس پا", "ساق پا", "پلنک", "زیربغل",
    "پشت پا", "جلوی پا", "هیپ تراست", "پرس دمبل", "اسکات از جلو"
]

REP_PERCENTAGE_DATA = [ 
    (1,   100),
    (2,    95),
    (4,    90),
    (6,    85),
    (8,    80),
    (10,   75),
    (11,   70),  # Typically 11–12 ~70%
    (12,   70),
    (13,   65),  # Typically 13–15 ~65%
    (14,   65),
    (15,   65),
    (16,   60),  # Typically 16–20 ~60%
    (17,   60),
    (18,   60),
    (19,   60),
    (20,   60),
    (25,   50),  # Broad range for higher reps ~50–55%
    (30,   40),
    (35,   35),
]

CATEGORIES_OPTIONS = {
        "قدرت" : {
            "قدرت نسبی": {
                "title":"تست قدرت نسبی", 
                "xaxis_title": "تاریخ",
                "yaxis_title_options":[
                    "میزان قدرت نسبی",
                    "یک تکرار بیشینه",
                ],
                "xaxis": "test_date",
                "yaxis_options":[
                    "relative_strength",
                    "one_repetition_maximum",
                ],

            },   
        },
        "استقامت" : {
            "۶-دقیقه": {
                "title":"تست ۶-دقیقه", 
                "xaxis_title": "تاریخ",
                "yaxis_title_options":[
                    "vo2max",
                ],
                "xaxis": "test_date",
                "yaxis_options":[
                    "vo2max",
                ]
            },
            "cooper": {
                "title":"cooper ",
                "xaxis_title": "تاریخ", 
                "yaxis_title_options":[
                    "vo2max",
                ],
                "xaxis": "test_date",
                "yaxis_options":[
                    "vo2max",
                ],
            }   
        },
        "بی-هوازی" : { 
            "افت-عملکرد": {
                "title":"تست افت-عملکرد", 
                "xaxis_title": "تاریخ",
                "yaxis_title_options":[
                    "میزان افت عملکرد",
                    "درصد افت عملکرد",
                ],
                "xaxis": "test_date",
                "yaxis_options":[
                    "performance_decrease",
                    "performance_perc",
                ],

            },
            "RAST": {
                "title":"تست RAST", 
                "xaxis_title": "تاریخ",
                "yaxis_title_options":[
                    "توان اوج",
                    "توان میانگین",
                    "توان کل",
                    "شاخص خستگی",
                ],
                "xaxis": "test_date",
                "yaxis_options":[
                    "peak_power",
                    "average_power",
                    "total_power",
                    "fatigue_index",
                ],
            },
            "wingate": {
                "title":"تست wingate", 
                "xaxis_title": "تاریخ",
                "yaxis_title_options":[
                    "توان اوج",
                    "توان میانگین",
                    "توان کل",
                    "شاخص خستگی",
                ],
                "xaxis": "test_date",
                "yaxis_options":[
                    "peak_power",
                    "average_power",
                    "total_power",
                    "fatigue_index",
                ],
            },
            "burpee": {
                "title":"تست burpee", 
                "xaxis_title": "تاریخ",
                "yaxis_title_options":[
                    "تعداد برپی",
                ],
                "xaxis": "test_date",
                "yaxis_options":[
                    "burpee_count",
                ],
            },
        },
        "چابکی" : {
            "ویژه-کشتی": {
                "title":"تست ویژه کشتی", 
                "xaxis_title": "تاریخ",
                "yaxis_title_options":[
                    "زمان ویژه کشتی ",
                ],
                "xaxis": "test_date",
                "yaxis_options":[
                    "wrestle_specific_duration",
                ],
            },
            "خرسی": {
                "title":"تست خرسی", 
                "xaxis_title": "تاریخ",
                "yaxis_title_options":[
                    "زمان خرسی",
                ],
                "xaxis": "test_date",
                "yaxis_options":[
                    "bear_duration",
                ],
            },
            "منطقه": {
                "title":"تست منطقه", 
                "xaxis_title": "تاریخ",
                "yaxis_title_options":[
                    "زمان منطقه",
                ],
                "xaxis": "test_date",
                "yaxis_options":[
                    "zone_duration",
                ],
            }, 
            "T": {
                "title":"تست T", 
                "xaxis_title": "تاریخ",
                "yaxis_title_options":[
                    "زمان T",
                ],
                "xaxis": "test_date",
                "yaxis_options":[
                    "T_duration",
                ],
            }, 
            "illinois": {
                "title":"تست illinois",
                "xaxis_title": "تاریخ",
                "yaxis_title_options":[
                    "زمان illinois",
                ],
                "xaxis": "test_date",
                "yaxis_options":[
                    "illinois_duration",
                ],
            },
        },
        "انعطاف پذیری" : {
            "sit&reach": {
                "title":"آزمون sit&reach",
                "xaxis_title": "تاریخ",
                "yaxis_title_options":[
                    "طول sit&reach",
                ],
                "xaxis": "test_date",
                "yaxis_options":[
                    "sit_reach_distance",
                ],
            },
            "بالا-آوردن-شانه": {
                "title":"آزمون بالا آوردن شانه",
                "xaxis_title": "تاریخ",
                "yaxis_title_options":[
                    "طول بالا آوردن شانه",
                ],
                "xaxis": "test_date",
                "yaxis_options":[
                    "shoulder_lift_distance",
                ],
            },
              "باز-شدن-بالا-تنه": {
                "title":"آزمون باز شدن بالا تنه",
                "xaxis_title": "تاریخ",
                "yaxis_title_options":[
                    "باز شدن بالا تنه",
                ],
                "xaxis": "test_date",
                "yaxis_options":[
                    "upper_body_opening_distance",
                ],
            },
        },
        "استقامت عضلانی" : {
            "دراز-نشست": {
                "title":"آزمون دراز و نشست",
                "xaxis_title": "تاریخ",
                "yaxis_title_options":[
                    "تعداد دراز و نشست",
                ],
                "xaxis": "test_date",
                "yaxis_options":[
                    "situp_reps",
                ],
            },
            "بارفیکس": {
                "title":"آزمون بارفیکس",
                "xaxis_title": "تاریخ",
                "yaxis_title_options":[
                    "تعداد بارفیکس",
                ],
                "xaxis": "test_date",
                "yaxis_options":[
                    "pullup_reps",
                ],
            },
            "دیپ-پارالل": {
                "title":"آزمون دیپ پارالل",
                "xaxis_title": "تاریخ",
                "yaxis_title_options":[
                    "تعداد دیپ پارالل",
                ],
                "xaxis": "test_date",
                "yaxis_options":[
                    "dip_parallel_reps",
                ],
            },
        },

    }
