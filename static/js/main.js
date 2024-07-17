const getObtionChart=async ()=>{
    try {
        const response=await fetch("http://127.0.0.1:8000/api/get_chart/");
        return await response.json()
    } catch (error) {
        alert(error);
    }
};

const initChart=async()=>{
    const myChart=echarts.init(document.getElementById("chart"));
    
    myChart.setOption(await getObtionChart());
    myChart.resize();
};

window.addEventListener("load", async()=>{
    await initChart();
});