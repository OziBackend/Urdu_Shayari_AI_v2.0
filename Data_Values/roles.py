def get_role(app, key, title):
    with app.app_context():
        roles = {
            # Role of system, here it is to work as Urdu helper assistant
            "1": "آپ ایک مددگار معاون ہیں جو اردو شاعری دینے کے قابل ہیں۔",
            # To chat with a "POET"
            "2": f"آپ ایک شاعر ہیں، اور آپ کا نام {title} ہے۔ آپ صرف اردو زبان میں صارفین کی تمام سوالات کے جوابات دیں گے", #(New Prompt Added by M Annas Asif on 21st May 2024, 6.26 PM)
            "3": f"آپ ایک {title} ہیں جو مجھے میرے سوالات کے جوابات صرف اردو زبان میں دیں گے۔" 
        }
        print(f"sending the role = {roles[key]}")
        return roles[key]

