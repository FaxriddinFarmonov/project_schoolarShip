

const viloyat= ["Toshkent", "Andijon", "Namangan","Farg'ona", "Sirdaryo", "Jizzax","Samarqand", "Qashqadaryo","Surxondaryo","Buxoro","Navoiy","Xorazm","Qoraqalpog'iston"];
const qoraqalpoq = ["Boʻzatov", "Taxiatosh", "Xoʻjayli", "Toʻrtkoʻl", "Taxtakoʻpir", "Shumanay","Qoraoʻzak", "Qoʻngʻirot", "Qanlikoʻl","Nukus", "Moʻynoq", "Kegeyli", "Ellikqalʼa","Chimboy", "Beruniy", "Amudaryo","Xaqlobod"];
const xorazm = ["Bogʻot", "Gurlan", "Xonqa","Hazorasp", "Xiva", "	Qoʻshkoʻpir","Shovot", "Urganch", "Yangiariq","Yangibozor", "Tuproqqalʼa"];
const navoiy = ["Konimex ", "Karmana ", "Qiziltepa", "Xatirchi", "Navbahor ", "Nurota","Tomdi ", "Uchquduq"];
const buxoro = ["Olot ", "Buxoro", "Gʻijduvon", "Jondor", "Kogon", "Qorakoʻl ","Qorovulbozor", "Peshku", "Romitan", "Shofirkon","Vobkent"];
const surxon = ["Angor ", "Boysun", "Denov", "Jarqoʻrgʻon", "", "Qumqoʻrgʻon ","Muzrabot", "Oltinsoy ", "Denov", "Sariosiyo", "Sherobod", "Shoʻrchi ","Termiz", "Uzun "];
const qashqar = ["Chiroqchi", "Dehqonobod", "Gʻuzor", "Qamashi", "Qarshi", "Koson","	Kasbi", "Kitob", "Mirishkor","Muborak", "Nishon ", "Shahrisabz", "Yakkabogʻ","Koʻkdala"];
const samarqand= ["Bulungʻur", "Ishtixon", "Jomboy ","Kattaqoʻrgʻon ", "Qoʻshrabot", "Narpay ","Nurobod", "Oqdaryo", "Paxtachi","Payariq", "Pastdargʻom", "Samarqand", "Toyloq","	Urgut"];
const jizzax = ["Arnasoy ", "Baxmal", "	Doʻstlik ", "Forish", "Sharof Rashidov", "Gʻallaorol","Mirzachoʻl ", "Paxtakor", "Yangiobod ", "Zomin","Zafarobod", "	Zarbdor"];
const sirdaryo = ["Oqoltin", "Boyovut", "Guliston", "Xovos", "Mirzaobod", "Sayxunobod","Sardoba", "Sirdaryo", "Yangiyer", "Shirin","Guliston shahri"];
const Fargona = ["Oltiariq ", "Bagʻdod", "Beshariq", "Buvayda", "Dangʻara", "Fargʻona","Furqat", "Qoʻshtepa", "Quva ", "Rishton", "Soʻx", "Toshloq","Uchkoʻprik ", "Oʻzbekiston","	Yozyovon ", "Quvasoy ","Zarkent","marg'ilon"];
const Andijon = ["Andijon ", "Asaka", "Baliqchi", "Bo'ston ", "Buloqboshi", "Izboskan","Jalaquduq ", "Xoʻjaobod", "Qoʻrgʻontepa ", "Marhamat", "Oltinkoʻl","Paxtaobod", "Shahrixon", "Ulugʻnor"];
const Toshkentv = ["Toshkent_shahar","Bekobod", "Boʻstonliq", "Boʻka", "Chinoz", "Qibray", "	Ohangaron","Oqqoʻrgʻon", "Parkent", "Piskent", "Quyi_chirchiq","Oʻrta_Chirchiq", "Yangiyoʻl", "Yuqori Chirchiq", "Zangiota ",];
const namangan = ["Chortoq", "Chortoq", "Kosonsoy", "Mingbuloq ", "Namangan ", "Norin ","Pop", "Toʻraqoʻrgʻon", "	Uchqoʻrgʻon ", "Uychi ","Yangiqoʻrgʻon"];
let slc1=document.getElementById("slc1");
let slc2=document.getElementById("slc2");


viloyat.forEach(function addVil(item){
    let opt =document.createElement('option');
    opt.text=item;
    opt.value=item;
    slc1.appendChild(opt);
});
slc1.onchange=function(){
    slc2.innerHTML="<option></option>"
    if(this.value=="Toshkent shahar"){
        addToslc2(toshkent);
    }
    if(this.value=="Xorazm"){
        addToslc2(xorazm);
    }
    if(this.value=="Qoraqalpog'iston"){
        addToslc2(qoraqalpoq);
    }
    if(this.value=="Navoiy"){
        addToslc2(navoiy);
    }
    if(this.value=="Buxoro"){
        addToslc2(buxoro);
    }
    if(this.value=="Surxondaryo"){
        addToslc2(surxon);
    }
    if(this.value=="Qashqadaryo"){
        addToslc2(qashqar);
    }
    if(this.value=="Samarqand"){
        addToslc2(samarqand);
    }
    if(this.value=="Jizzax"){
        addToslc2(jizzax);
    }
    if(this.value=="Sirdaryo"){
        addToslc2(sirdaryo);
    }
    if(this.value=="Farg'ona"){
        addToslc2(Fargona);
    }
    if(this.value=="Namangan"){
        addToslc2(namangan);
    }
    if(this.value=="Andijon"){
        addToslc2(Andijon);
    }
    if(this.value=="Toshkent"){
        addToslc2(Toshkentv);
    }
}
function addToslc2(arr){
    arr.forEach ( function (item){
            let opt =document.createElement('option');
            opt.text=item;
            opt.value=item;
            slc2.appendChild(opt); 
});
    }
