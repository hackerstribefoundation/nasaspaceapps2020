#The Main Application Code
#Modules
from tkinter import *
from datetime import datetime, date, timedelta
from fpdf import FPDF
from tkinter import filedialog

#Constants
gen=["-select-","M","F"]
pro=["-select-","Mussle Gain","Lose Fat","Maintain Weight"]
activ=['-select-','Sedentary','Lightly Active','Moderately Active','Very Avtive','Extra Active']
sys=['-select-','Metric', 'Imperial']
global activity_factor,nutrient_value,sleep_hour,time
time=datetime.strptime('00:00:00','%H:%M:%S').time()
activity_factor={'Sedentary':1.2,
                'Lightly Active':1.375,
                'Moderately Active':1.55,
                'Very Avtive':1.725,
                'Extra Active':1.9}
nutrient_value={'Carbohydrate':4,
                'Protein':4,
                'Fat':9}
sleep_hour={'newborn':15,
            'infants':13.5,
            'toddler':12,
            'pre-school':12,
            'elementary-age':10.5,
            'teens':9,
            'adults':7.5}

#Window Setup
root=Tk()
root.geometry("750x690")
root.title("Your Assistantant (Sleep Scheduler and Diet Planner) v1.0")
mlabel=Label(root,text='The Bug Slayers',font=("consolas",24,'bold'))
mlabel.pack(side=TOP)

#Functions
def BMR_male(system,weight,height,age):
    if system=='Metric':
        bmr_value=66.5+(13.75*weight)+(5.003*height)-(6.755*age)
    elif system=='Imperial':
        bmr_value=66+(6.2*weight)+(12.7*height)-(6.76*age)
    return bmr_value

def BMR_female(system,weight,height,age):
    if system=='Metric':
        bmr_value=655.1+(9.563*weight)+(1.85*height)-(4.676*age)
    elif system=='Imperial':
        bmr_value=655.1+(4.35*weight)+(4.7*height)-(4.7*age)
    return bmr_value

def calorie_calculator(system,weight,height,age,activity_status,sex):
    if sex=='M':
        bmr_value=BMR_male(system,weight,height,age)
    elif sex=='F':
        bmr_value=BMR_female(system,weight,height,age)
    
    calorie_required=bmr_value*activity_factor[activity_status]
    
    return calorie_required

def nutrient_breaker(program,daily_calorie_need):
    if program=="Mussle Gain":
#-------------------Mussle Gain Program-----------------------------
#-------------------Calorie Breakdown Nutrients-wise----------------
        carbohydrate=(daily_calorie_need*60)/100
        protein=(daily_calorie_need*35)/100
        fat=daily_calorie_need-carbohydrate-protein
#-------------------Breakdown in gms--------------------------------
        carb_gm=round(carbohydrate/4)
        prot_gm=round(protein/4)
        fat_gm=round(fat/9)
    elif program=="Maintain Weight":
#-------------------Maintain Weight Program-------------------------
#-------------------Calorie Breakdown Nutrients-wise----------------
        carbohydrate=(daily_calorie_need*50)/100
        protein=(daily_calorie_need*25)/100
        fat=daily_calorie_need-carbohydrate-protein
#-------------------Breakdown in gms--------------------------------
        carb_gm=round(carbohydrate/4)
        prot_gm=round(protein/4)
        fat_gm=round(fat/9)
    elif program=="Lose Fat":
#-------------------Weight Lose Program-----------------------------
#-------------------Calorie Breakdown Nutrients-wise----------------
        carbohydrate=(daily_calorie_need*10)/100
        protein=(daily_calorie_need*50)/100
        fat=daily_calorie_need-carbohydrate-protein
#-------------------Breakdown in gms--------------------------------
        carb_gm=round(carbohydrate/4)
        prot_gm=round(protein/4)
        fat_gm=round(fat/9)

    return carb_gm,prot_gm,fat_gm

def Age_group(age):
    if age>=0 and age<=0.25:
        agg=1
    elif age>0.25 and age<=1:
        agg=2
    elif age>1 and age<=2:
        agg=3
    elif age>2 and age<=5:
        agg=4
    elif age>5 and age<=12:
        agg=5
    elif age>12 and age<=18:
        agg=6
    else:
        agg=7
    return agg

def sleep_requirement(agg):
    if agg==1:
#-------------------Newborns----------------------------------------
        required_hour=sleep_hour['newborn']
    elif agg==2:
#-------------------Infants-----------------------------------------
        required_hour=sleep_hour['infants']
    elif agg==3:
#-------------------Toddler-----------------------------------------
        required_hour=sleep_hour['toddler']
    elif agg==4:
#-------------------Pre-School--------------------------------------
        required_hour=sleep_hour['pre-school']
    elif agg==5:
#-------------------Elementary-Age----------------------------------
        required_hour=sleep_hour['elementary-age']
    elif agg==6:
#-------------------Teens-------------------------------------------
        required_hour=sleep_hour['teens']
    elif agg==7:
#-------------------Adults-----------------------------
        required_hour=sleep_hour['adults']
    sleep_cycle=int(required_hour/1.5)
    return required_hour,sleep_cycle

def Sleep_Customiser(work_start,work_end,preparation,refresh,required_hour,sleep_buffer):
#-------------------Input Formatting--------------------------------
    work_start_format=datetime.strptime(work_start, '%H:%M:%S').time()
    work_end_format=datetime.strptime(work_end, '%H:%M:%S').time()
#-------------------Work Hour---------------------------------------
    temp_start=datetime.combine(date.today(),work_start_format)-datetime.combine(date.today(),time)
    temp_end=datetime.combine(date.today(),work_end_format)-datetime.combine(date.today(),time)
    if temp_end>temp_start:
        work_hour=datetime.combine(date.today(),work_end_format)-datetime.combine(datetime.today(),work_start_format)
    elif temp_end<temp_start:
        work_hour=datetime.combine(date.today()+timedelta(days=1),work_end_format)-datetime.combine(datetime.today(),work_start_format)
#------------------Min Active Hour, Total Sleep Hour, Available Sleep Hours---------------
    non_sleep_hours=work_hour+timedelta(hours=preparation)+timedelta(hours=refresh)
    total_sleep_hours=timedelta(hours=required_hour)+timedelta(minutes=sleep_buffer)
    available_sleep_time=timedelta(hours=24)-non_sleep_hours
#-----------------Start and End time of Sleep---------------------------------------------
    start_sleep_avail=(datetime.combine(date.today(),work_end_format)+timedelta(hours=refresh)).time()
    end_sleep_avail=(datetime.combine(date.today(),work_start_format)-timedelta(hours=preparation)-total_sleep_hours).time()
#-----------------Continuity checker------------------------------------------------------
    temp_start_avail=datetime.combine(date.today(),start_sleep_avail)-datetime.combine(date.today(),time)
    temp_end_avail=datetime.combine(date.today(),end_sleep_avail)-datetime.combine(date.today(),time)
    if temp_end_avail<temp_start_avail:
        temp_end_avail=datetime.combine(date.today()+timedelta(days=1),end_sleep_avail)-datetime.combine(date.today(),time)
#-----------------Time Slot Storage--------------------------------------------------------
    start_list=[]
    end_list=[]
#-----------------Work Load Checking-------------------------------------------------------
    if total_sleep_hours>available_sleep_time:
#-----------------Less Sleep Time----------------------------------------------------------
        return 'Insufficient Sleep Hour. Reduce Your Activity Hour'
    else:
        while temp_start_avail<=temp_end_avail:
            ts=(datetime.combine(date.today(),time)+temp_start_avail).time()
            te=(datetime.combine(date.today(),time)+temp_start_avail+total_sleep_hours).time()
            start_list.append(ts.strftime('%H:%M:%S'))
            end_list.append(te.strftime("%H:%M:%S"))
            temp_start_avail=temp_start_avail+timedelta(minutes=30)
        return start_list,end_list
def save(name,age,sex,system,height,weight,activity_status,program,work_start,work_end,preparation,refresh,required_hour,sleep_buffer,sleep_cycle,cus,calorie_required,nut,title):
#------------------------Instance Creation & Addition of First Page-------------------
    pdf=FPDF()
    pdf.add_page()
    pdf.set_font("Arial",'B',20) 
#------------------------Create Cells & Add Data--------------------------------------
    pdf.cell(200, 10, txt = "Sleep Schedule and Nutrition Report",ln = 1, align = 'C')
    pdf.set_font("Arial", size = 13)
    pdf.cell(200, 10, txt = "________________________________________________________________________", ln=2, align='L') 
    pdf.cell(200, 10, txt = "Name: "+name, ln=3, align='L')
    pdf.cell(200, 10, txt = "Age:"+str(age)+"                                             Sex:"+sex+"                                      System: "+system, ln=4, align='L')
    if system=='Metric':
        pdf.cell(200, 10, txt = "Weight: "+str(weight)+" kg"+"                                                                                  Height: "+str(int(height))+" cm", ln=5, align='L')
    elif system=='Imperial':
        pdf.cell(200, 10, txt = "Weight: "+str(weight)+" lbs."+"                                                                          Height: "+str(int(height))+" inches", ln=5, align='L')
    pdf.cell(200, 10, txt = "Activity Status: "+activity_status+"                                              Program: "+program, ln=6, align='L')
    pdf.cell(200, 10, txt = "Work Start Time                               : "+work_start, ln=7, align='L')
    pdf.cell(200, 10, txt = "Work End Time                                : "+work_end, ln=8, align='L')
    pdf.cell(200, 10, txt = "Preparation Time After Waking Up  : "+str(preparation)+" hrs.", ln=9, align='L')
    pdf.cell(200, 10, txt = "Refresh Time After Work                 : "+str(refresh)+" hrs.", ln=9, align='L')
    pdf.cell(200, 10, txt = "Buffer Time Before Sleep                : "+str(sleep_buffer)+" mins.", ln=9, align='L')
    pdf.cell(200, 10, txt = "________________________________________________________________________", ln=10, align='L')
    pdf.set_font("Arial",'B',16)
    pdf.cell(200, 10, txt = "Sleep Report", ln=11, align='C')
    pdf.set_font("Arial", size = 13) 
    pdf.cell(200, 10, txt = "Daily Required Sleep Hour : "+str(required_hour)+" hrs.", ln=12, align='L') 
    pdf.cell(200, 10, txt = "Number of Sleep Cycles (90 min each) : "+str(sleep_cycle), ln=13, align='L')
    try:
        pdf.cell(200, 10, txt = cus, ln=14, align='L')
    except:
        pdf.cell(200, 10, txt = "Your Customised Sleeping Slots: ", ln=14, align='L')
        for i in range(len(cus[0])):
            pdf.cell(200, 10, txt = "Sleep: "+cus[0][i]+"           Wake: "+cus[1][i], ln=15, align='L')
    pdf.cell(200, 10, txt = "________________________________________________________________________", ln=16, align='L')
    pdf.cell(200, 10, txt = "A Well Spent Day Bring Happy Sleep. Sweet Dreems.", ln=17, align='L')
    pdf.set_font("Arial",'B',20)
    pdf.cell(200, 10, txt = "Diet Report", ln=18, align='C')
    pdf.set_font("Arial", size = 13)
    pdf.cell(200, 10, txt = "Daily Calorie Requirement : "+str(round(calorie_required)), ln=19, align='L')
    pdf.cell(200, 10, txt = "Your Customised Nurtrient Distribution : ", ln=20, align='L')
    pdf.cell(200, 10, txt = "Carbohydrate : "+str(nut[0])+' gm', ln=21, align='L')
    pdf.cell(200, 10, txt = "Protein            : "+str(nut[1])+' gm', ln=22, align='L')
    pdf.cell(200, 10, txt = "Fat                  : "+str(nut[2])+' gm', ln=23, align='L')
    pdf.cell(200, 10, txt = "________________________________________________________________________", ln=16, align='L')
        
    
#------------------------Save .pdf file-----------------------------------------------   
    pdf.output(title)

def Gen_But():
    name=nam.get()
    age=float(ag.get())
    sex=sx.get()
    system=sy.get()
    height=float(ht.get())
    weight=float(wt.get())
    activity_status=act.get()
    program=prog.get()
    work_start=ws.get()
    work_end=we.get()
    preparation=float(prep.get())
    refresh=float(ref.get())
    sleep_buffer=int(sb.get())
    sr=sleep_requirement(Age_group(age))
    required_hour=sr[0]
    sleep_cycle=sr[1]
    cus=Sleep_Customiser(work_start,work_end,preparation,refresh,required_hour,sleep_buffer)
    calorie_required=calorie_calculator(system,weight,height,age,activity_status,sex)
    nut=nutrient_breaker(program,calorie_required)
    title=filedialog.asksaveasfilename()
    save(name, age, sex, system, height, weight, activity_status, program, work_start, work_end, preparation, refresh, required_hour, sleep_buffer, sleep_cycle,cus,calorie_required,nut,title)


#Input Fields & Input Variables
nam=StringVar()
ag=StringVar()
sx=StringVar(root)
sx.set(gen[0])
sy=StringVar(root)
sy.set(sys[0])
prog=StringVar(root)
prog.set(pro[0])
act=StringVar(root)
act.set(activ[0])
wt=StringVar()
ht=StringVar()
ws=StringVar()
we=StringVar()
sb=StringVar()
prep=StringVar()
ref=StringVar()

#Name Field
nl=Label(root,text='Name',font=("consolas",15,'bold'))
nl.place(x=5,y=60)
n=Entry(root,textvariable=nam,width=60,bg='powder blue',bd=4,font=("consolas",15,'bold'))
n.place(x=60,y=60)
#Age Field
al=Label(root,text='Age',font=("consolas",15,'bold'))
al.place(x=5,y=120)
a=Entry(root,textvariable=ag,font=("consolas",15,'bold'),width=10,bg='powder blue',bd=4)
a.place(x=60,y=120)
#Sex Field
sl=Label(root,text='Sex',font=("consolas",15,'bold'))
sl.place(x=220,y=120)
s=OptionMenu(root,sx,*gen)
s.config(bg='powder blue',width=12,bd=4,font=("consolas",12,'bold'),relief='sunken')
s.place(x=275,y=118)
#System Field
syl=Label(root,text='System',font=("consolas",15,'bold'))
syl.place(x=486,y=120)
sye=OptionMenu(root,sy,*sys)
sye.config(bg='powder blue',width=12,bd=4,font=("consolas",12,'bold'),relief='sunken')
sye.place(x=576,y=118)
#Weight Field
wl=Label(root,text='Weight',font=("consolas",15,'bold'))
wl.place(x=5,y=180)
w=Entry(root,textvariable=wt,font=("consolas",15,'bold'),width=18,bg='powder blue',bd=4)
w.place(x=100,y=180)
#Height Field
hl=Label(root,text='Height',font=("consolas",15,'bold'))
hl.place(x=462,y=180)
h=Entry(root,textvariable=ht,font=("consolas",15,'bold'),width=16,bg='powder blue',bd=4)
h.place(x=546,y=180)
#Activity Status
acl=Label(root,text='Activity',font=("consolas",15,'bold'))
acl.place(x=5,y=240)
ac=OptionMenu(root,act,*activ)
ac.config(bg='powder blue',width=18,bd=4,font=("consolas",12,'bold'),relief='sunken')
ac.place(x=100,y=238)
#Program Selection
pl=Label(root,text='Program',font=("consolas",15,'bold'))
pl.place(x=462,y=240)
p=OptionMenu(root,prog,*pro)
p.config(bg='powder blue',width=15,bd=4,font=("consolas",12,'bold'),relief='sunken')
p.place(x=547,y=238)
#Work Start Field
wsl=Label(root,text='Work Start Time(HH:MM:SS)',font=("consolas",15,'bold'))
wsl.place(x=5,y=300)
wks=Entry(root,textvariable=ws,font=("consolas",15,'bold'),width=25,bg='powder blue',bd=4)
wks.place(x=441,y=300)
#Work End Field
wel=Label(root,text='Work End Time(HH:MM:SS)',font=("consolas",15,'bold'))
wel.place(x=5,y=360)
wke=Entry(root,textvariable=we,font=("consolas",15,'bold'),width=25,bg='powder blue',bd=4)
wke.place(x=441,y=360)
#Preparation time Field
prel=Label(root,text='Preparation Time After Waking Up(hour)',font=("consolas",15,'bold'))
prel.place(x=5,y=420)
pr=Entry(root,textvariable=prep,font=("consolas",15,'bold'),width=25,bg='powder blue',bd=4)
pr.place(x=441,y=420)
#Preparation time Field
rel=Label(root,text='Refresh Time After Work(hour)',font=("consolas",15,'bold'))
rel.place(x=5,y=480)
r=Entry(root,textvariable=ref,font=("consolas",15,'bold'),width=25,bg='powder blue',bd=4)
r.place(x=441,y=480)
#Preparation time Field
sbl=Label(root,text='Buffer Time Before Sleep(minutes)',font=("consolas",15,'bold'))
sbl.place(x=5,y=540)
slb=Entry(root,textvariable=sb,font=("consolas",15,'bold'),width=25,bg='powder blue',bd=4)
slb.place(x=441,y=540)
#Instruction Label
il=Label(root,text='If using metric system, use kg and cm. If using imperial system, use lbs and inches.For Time use 24hrs format.',font=('arial',10),fg='blue',bg='yellow')
il.place(x=45,y=600)
#Save Button
savebut=Button(root,padx=10,pady=3,bd=4,fg='white',text="Generate Report",font=("Courier New",12,'bold'),bg='royalblue',command=Gen_But)
savebut.place(x=278,y=635)

root.mainloop()
