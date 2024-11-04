<script>
    document.querySelectorAll('.region-btn').forEach(button = >{
        button.addEventListener('click', function() {
            // 移除所有按钮的激活状态
            document.querySelectorAll('.region-btn').forEach(btn => btn.classList.remove('active'));
            // 为点击的按钮添加激活状态
            this.classList.add('active');
        });
    }); 
</script>
