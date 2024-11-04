/* jshint esversion: 6 */
/* jshint browser: true */
/* jshint browser: true, devel: true */
/* global loginUrl, logoutUrl */


function logoutUser() {
    // 直接跳转到登录页面
    "use strict";
    window.location.href = loginUrl;
}

// 切换到编辑模式
document.getElementById('edit-btn').addEventListener('click', function() {
    "use strict";
    document.getElementById('edit-form').style.display = 'block';
    document.getElementById('edit-btn').style.display = 'none';
    document.getElementById('logout-btn').style.display = 'none';

    // 隐藏默认信息展示
    document.querySelector('.profile-card').style.display = 'none';

    // 清空密码相关输入框
    document.getElementById('current-password').value = '';
    document.getElementById('new-password').value = '';
    document.getElementById('confirm-password').value = '';
    document.getElementById('warningMessage').style.display = 'none'; // 隐藏警告信息
});




document.querySelector('.info-form').addEventListener('submit', function(event) {
    "use strict";
    event.preventDefault();  // 阻止表单的默认提交

    const originalUsername = document.getElementById('username').textContent;
    const originalEmail = document.getElementById('email').textContent;
    const originalPhone = document.getElementById('phone').textContent;
    const originalSignature = document.getElementById('signature').textContent;

    const updatedUsername = document.getElementById('edit-username').value;
    const updatedEmail = document.getElementById('edit-email').value;
    const updatedPhone = document.getElementById('edit-phone').value;
    const updatedSignature = document.getElementById('edit-signature').value;

    // 检查密码修改部分
    const currentPassword = document.getElementById('current-password').value;
    const newPassword = document.getElementById('new-password').value;
    const confirmPassword = document.getElementById('confirm-password').value;

    const warningMessage = document.getElementById('warningMessage');
    warningMessage.style.display = 'none';
    warningMessage.textContent = '';

    // 清空表单数据
    const formData = new FormData(this);

    // 检查是否要修改密码
    let passwordValid = true;  // 标记密码格式是否有效

    if (currentPassword || newPassword || confirmPassword) {
        // 添加密码字段到 FormData
        formData.append('current_password', currentPassword);
        formData.append('new_password', newPassword);

        // 检查新密码与确认密码
        if (newPassword !== confirmPassword) {
            warningMessage.textContent = '新密码与确认密码不一致，请重新输入';
            warningMessage.style.display = 'block';
            passwordValid = false;  // 标记为无效
        }

        // 检查新密码长度
        if (newPassword.length < 6 || newPassword.length > 10) {
            warningMessage.textContent = '新密码长度要求为6-10位';
            warningMessage.style.display = 'block';
            passwordValid = false;  // 标记为无效
        }
    }

    // 如果密码格式不正确，终止后续操作
    if (!passwordValid) {
        return;  // 不提交表单
    }

    // 提交表单
    fetch(this.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': '{{ csrf_token }}'
        }
    }).then(response => {
        if (response.ok) {
            // 弹出修改完成弹窗
            document.getElementById('info-modal').style.display = 'block';

            // 更新页面显示
            document.getElementById('username').textContent = updatedUsername;
            document.getElementById('email').textContent = updatedEmail;
            document.getElementById('phone').textContent = updatedPhone;
            document.getElementById('signature').textContent = updatedSignature;

            // 更新头像
            const avatarPreview = document.getElementById('avatar-preview');
            if (avatarPreview.src) {
                document.getElementById('avatar').src = avatarPreview.src;
            }

            // 定时跳转到个人信息页面
            setTimeout(() => {
                window.location.href = this.action;  // 返回个人信息页面
            }, 1000);  // 1秒后跳转
        } else {
            return response.json().then(data => {
                if (data.error) {
                    warningMessage.textContent = data.error;  // 显示后端返回的错误信息
                    warningMessage.style.display = 'block';
                }
            });
        }
    }).catch(error => {
        console.error('Error during fetch:', error);
        warningMessage.textContent = '请求失败，请重试';
        warningMessage.style.display = 'block';
    });
});





// 放弃修改
document.getElementById('cancel-btn').addEventListener('click', function() {
    // 恢复到初始状态
    "use strict";
    document.getElementById('edit-form').reset();  // 重置表单数据

    // 隐藏编辑模式
    document.getElementById('edit-form').style.display = 'none';
    document.querySelector('.profile-card').style.display = 'flex';
    document.getElementById('edit-btn').style.display = 'inline-block';
    document.getElementById('logout-btn').style.display = 'inline-block';

    // 清空头像预览
    document.getElementById('avatar-preview').style.display = 'none';
    document.getElementById('avatar-upload').value = '';  // 清空文件上传输入框
});

// 头像上传预览
document.getElementById('avatar-upload').addEventListener('change', function(event) {
    "use strict";
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('avatar-preview').src = e.target.result;
            document.getElementById('avatar-preview').style.display = 'block';
        };
        reader.readAsDataURL(file);
    }
});

// 关闭弹窗
document.getElementById('close-modal-btn').addEventListener('click', function() {
    "use strict";
    document.getElementById('info-modal').style.display = 'none';
});

// 添加密码长度提示
const newPasswordInput = document.getElementById('new-password');
const passwordHint = document.createElement('small');
passwordHint.textContent = '密码长度要求为6-10位';
passwordHint.style.color = 'gray';
newPasswordInput.parentNode.appendChild(passwordHint);
