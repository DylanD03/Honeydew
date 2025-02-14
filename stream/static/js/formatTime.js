document.addEventListener("DOMContentLoaded", function () {
    // 获取所有时间元素
    const timeElements = document.querySelectorAll('.time-posted');
    
    timeElements.forEach((element) => {
      const isoTime = element.textContent.trim(); 
      const localTime = new Date(isoTime).toLocaleString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: true, 
        timeZoneName: 'short', 
      });
  
      element.textContent = localTime;
    });
  });
  