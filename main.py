from fastapi import FastAPI ,Path,HTTPException,Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal,Optional
import json
app=FastAPI()

class Patient(BaseModel):
    id:Annotated[str,Field(...,description='id of patient',examples=['P001'])]
    name:Annotated[str,Field(...,description='name of patient')]
    city:Annotated[str,Field(...,description='city of patient')]
    age:Annotated[int,Field(...,gt=0,lt=120,description='age of patient')]
    gender:Annotated[str,Literal['male','female','others'],Field(...)]
    height:Annotated[float,Field(...,gt=0,description='height')]
    weight:Annotated[float,Field(...,gt=0)]

    @computed_field
    @property
    def bmi(self)->float:
        bmi=round(self.weight/(self.height**2),2)
        return bmi
    
    @computed_field
    @property
    def verdict(self)->str:
        if self.bmi <18.5:
            return 'underweight'
        elif self.bmi<30:
            return 'normal'
        else:
            return 'obsese'

class Patient_update(BaseModel):
    name:Annotated[Optional[str],Field(default=None)]
    city:Annotated[Optional[str],Field(default=None)]
    age:Annotated[Optional[int],Field(default=None,gt=0)]
    gender:Annotated[Optional[str],Literal['male','female','others'],Field(default=None)]
    height:Annotated[Optional[str],Field(default=None,gt=0)]
    weight:Annotated[Optional[str],Field(default=None,gt=0)]


def load_data():
    with open('paitents.json','r') as f:
        data=json.load(f)
    return data

def save_data(data):
    with open('paitents.json','w') as f:
        json.dump(data,f)

@app.get("/")
async def hello():
    return {"message":"patient Management System API"}

@app.get("/about")
async def about():
    return {"message":"a fully functional api to manage your patient records"}

@app.get("/view")
async def view():
    data=load_data()
    return data

@app.get("/patient/{patient_id}")
async def view_patient(patient_id:str =Path(...,description="iD fo the patient",example='P001')):
    data=load_data()
    if patient_id in data:
        return data[patient_id]
    # return {'error':'patient not found'}
    raise HTTPException(status_code=404,detail='patient not found')

@app.get("/sort")
async def sort_patient(sort_by:str=Query(...,description='put Sorting order'),order:str=Query('asc',description='select the order')):
    valid_fileds=['height','weight','bmi']
    if sort_by not in valid_fileds:
        raise HTTPException(status_code=400,detail=f'invalid field {valid_fileds}')
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400,detail=f'invalid  order field ')
    data=load_data()
    sort_order=True if order=='desc' else False
    sort_value=sorted(data.values(),key=lambda x:x.get(sort_by,0),reverse=sort_order)
    return sort_value

@app.post('/create')
async def create_patient(patient: Patient):
    try:
        data = load_data()
        if patient.id in data:
            raise HTTPException(status_code=400, detail='patient already exists')
        data[patient.id] = patient.model_dump(exclude=['id'])
        save_data(data)
        return JSONResponse(status_code=201, content={'message': 'patient created successfully'})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put('/edit/{patient_id}')
async def update_patient(pateint_id:str,pateint_update:Patient_update):
    data=load_data()
    if pateint_id  not in data:
        raise HTTPException(status_code=404,detail='patient not found')
    existing_patient_info=data[pateint_id]
    updated_patient_info=pateint_update.model_dump(exclude_unset=True)
    for key,value in updated_patient_info.items():
        existing_patient_info[key]=value
    existing_patient_info['id']=pateint_id
    existing_patient_info_pydantic=Patient(**existing_patient_info)
    existing_patient_info_dict=existing_patient_info_pydantic.model_dump(exclude=['id'])
    data[pateint_id]=existing_patient_info_dict
    save_data(data)
    return JSONResponse(status_code=200,content={'message':'patient edited'})

@app.delete('/delete/{patient_id}')
async def del_patient(patient_id:str):
    data=load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404,detail='no pateint found')
    del data[patient_id]
    save_data(data)
    return JSONResponse(status_code=200,content='patient delated sucessfully')
