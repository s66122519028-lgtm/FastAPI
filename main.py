from fastapi import FastAPI, HTTPException
import requests

# สร้างแอป FastAPI
app = FastAPI(
    title="Zoo Visitors API",
    description="API สำหรับดึงข้อมูลสถิติผู้เข้าชมสวนสัตว์ ปี 2569 (Data.go.th)"
)

@app.get("/api/zoo-visitors")
def get_zoo_visitors():
    # Resource ID จากที่โจทย์กำหนด
    resource_id = "0ecc96cf-d914-42a1-b184-dbbd013c3c9c"
    
    # URL สำหรับดึงข้อมูลผ่าน CKAN Datastore API ของ Data.go.th
    url = f"https://data.go.th/api/3/action/datastore_search?resource_id={resource_id}&limit=5"
    
    try:
        # ดึงข้อมูลจาก Data.go.th
        response = requests.get(url)
        response.raise_for_status() 
        data = response.json()
        
        # ดึงเฉพาะส่วนที่เป็นรายการข้อมูลสถิติจริง (records)
        records = data.get("result", {}).get("records", [])
        
        # คืนค่าเป็น JSON ตามข้อกำหนดโจทย์ (ระบุแหล่งที่มา, ปีงบประมาณ, และข้อมูลจริง)
        return {
            "source": "องค์การสวนสัตว์แห่งประเทศไทย ในพระบรมราชูปถัมภ์ (อ้างอิงจาก Data.go.th)",
            "fiscal_year": "2569",
            "dataset_name": "รายงานสถิติจำนวนผู้เข้าชมสวนสัตว์ ปีงบประมาณ 2569",
            "data": records
        }
        
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"ไม่สามารถดึงข้อมูลจาก Data.go.th ได้: {str(e)}")