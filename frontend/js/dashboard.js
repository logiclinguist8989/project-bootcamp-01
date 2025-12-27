document.addEventListener('DOMContentLoaded', () => {
  const chestBtn = document.getElementById('openChest');
  const toast = document.getElementById('toast');
  const playBtn = document.querySelector('.btn--play');

  function showToast(msg){
    toast.textContent = msg;
    toast.style.display = 'block';
    setTimeout(()=>{ toast.style.display = 'none' }, 1600);
  }

  chestBtn?.addEventListener('click', () => {
    chestBtn.disabled = true;
    chestBtn.textContent = 'Opening...';
    setTimeout(()=>{
      chestBtn.disabled = false;
      chestBtn.textContent = 'Open Chest';
      showToast('You found 10 bananas! 🍌');
      // bump star count for demo
      const stars = document.getElementById('starsCount');
      stars.textContent = String(Number(stars.textContent || '0') + 10);
    }, 900);
  });

  playBtn?.addEventListener('click', () => {
    showToast('Starting Alphabet Adventure — good luck!');
  });
});