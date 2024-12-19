document.addEventListener("DOMContentLoaded", function () {
  // 存储筛选条件，用于更新隐藏表单
  const filters = {};

  // 筛选条件按钮事件
  document.querySelectorAll(".region-btn").forEach((button) => {
    button.addEventListener("click", () => {
      const filter = button.getAttribute("data-filter");
      const value = button.getAttribute("data-value");

      // 更新按钮样式：移除当前组的所有按钮的 active 样式
      document
        .querySelectorAll(`.region-btn[data-filter="${filter}"]`)
        .forEach((btn) => btn.classList.remove("active"));
      // 为当前点击的按钮添加 active 样式
      button.classList.add("active");

      // 更新隐藏表单中的筛选值
      const hiddenInput = document.querySelector(`input[name="${filter}"]`);
      if (hiddenInput) {
        hiddenInput.value = value;
      }
    });
  });
});
