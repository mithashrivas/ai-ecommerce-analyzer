const ctx=document.getElementById('chart');

new Chart(ctx,{

type:'bar',

data:{

labels:['Demand','Competition','Profit'],

datasets:[{

label:'Analysis',

data:[90,60,28]

}]

},

options:{

responsive:true

}

});