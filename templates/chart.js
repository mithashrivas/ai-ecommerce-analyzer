const ctx = document.getElementById('myChart');

new Chart(ctx,{
type:'pie',

data:{
labels:['Demand','Profit','Selling'],

datasets:[{

data:[60,20,20]

}]
}
});