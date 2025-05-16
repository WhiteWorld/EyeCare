import rumps
import time
import threading
import logging
from timers import EyeTimers
from notifications import eye_rest_reminder, eye_drop_reminder

class EyeCareApp(rumps.App):
    def __init__(self):
        super(EyeCareApp, self).__init__('Eye Care', title='Eye Care')
        self.eye_rest_interval = 20 * 60  # 默认20分钟
        self.eye_drop_interval = 60 * 60  # 默认60分钟
        self.timers = EyeTimers(self.eye_rest_interval, self.eye_drop_interval, eye_rest_reminder, eye_drop_reminder)
        # self.start_timers() # 应用启动时不自动开始计时器
        # 添加菜单项
        self.set_rest_interval_menu = rumps.MenuItem('设置休息倒计时')
        self.set_drop_interval_menu = rumps.MenuItem('设置眼药水倒计时')

        self.rest_countdown_display = rumps.MenuItem('休息倒计时: 计算中...')
        self.drop_countdown_display = rumps.MenuItem('眼药水倒计时: 计算中...')
        self.menu = [self.set_rest_interval_menu, self.set_drop_interval_menu, self.rest_countdown_display, self.drop_countdown_display]
        self.set_rest_interval_menu.set_callback(self.set_rest_interval)
        self.set_drop_interval_menu.set_callback(self.set_drop_interval)

        # 设置菜单显示回调以触发更新
        self.update_countdowns()

    def set_rest_interval(self, sender):
        self.update_countdowns()
        window = rumps.Window(
            message='设置休息倒计时(分钟):\n格式示例: 20',
            title='设置休息倒计时', 
            default_text=str(self.eye_rest_interval // 60),
            dimensions=(40, 20),
            cancel=True,
            ok='确定'
        )
        response = window.run()
        if response.clicked and response.text:
            try:
                minutes = int(response.text)
                self.eye_rest_interval = minutes * 60
                self.timers.set_rest_interval(self.eye_rest_interval)
                self.timers.cancel_rest_timer()
                if hasattr(response, 'text2') and response.text2 in ['0', '1']:
                    periodic = response.text2 == '1'
                    self.timers.start_rest_timer(periodic=periodic)
                    if periodic:
                        self.rest_countdown_display.title = f'休息倒计时(周期): {rest_remaining_time}'
                else:
                    self.timers.start_rest_timer(periodic=False)
            except ValueError:
                rumps.notification('错误', '请输入有效的数字！', '')

    def set_drop_interval(self, sender):
        self.update_countdowns()
        window = rumps.Window(
            message='设置眼药水倒计时(分钟):\n格式示例: 60',
            title='设置眼药水倒计时', 
            default_text=str(self.eye_drop_interval // 60),
            dimensions=(40, 20),
            cancel=True,
            ok='确定'
        )
        response = window.run()
        if response.clicked and response.text:
            try:
                minutes = int(response.text)
                self.eye_drop_interval = minutes * 60
                self.timers.set_drop_interval(self.eye_drop_interval)
                self.timers.cancel_drop_timer()
                if hasattr(response, 'text2') and response.text2 in ['0', '1']:
                    periodic = response.text2 == '1'
                    self.timers.start_drop_timer(periodic=periodic)
                    if periodic:
                        self.drop_countdown_display.title = f'眼药水倒计时(周期): {drop_remaining_time}'
                else:
                    self.timers.start_drop_timer(periodic=False)
            except ValueError:
                rumps.notification('错误', '请输入有效的数字！', '')

    def start_timers(self, periodic_rest=False, periodic_drop=False):
        # EyeTimers now takes callbacks in __init__
        # start_timers in EyeTimers will start both individual timers
        self.timers.start_timers(periodic_rest=periodic_rest, periodic_drop=periodic_drop)


    def update_countdowns(self, _=None): # 添加一个可选参数 _
        if not hasattr(self, 'logging_configured'):
            # import logging
            logging.basicConfig(level=logging.INFO)
            self.logging_configured = True
        if hasattr(self, 'menu') and self.menu is not None:
            rest_remaining_time = self.timers.get_remaining_time('rest')
            self.rest_countdown_display.title = f'休息倒计时: {rest_remaining_time}'

            drop_remaining_time = self.timers.get_remaining_time('drop')
            self.drop_countdown_display.title = f'眼药水倒计时: {drop_remaining_time}'

        # 确保定时器持续运行（移除重复创建限制）
        if not hasattr(self, '_update_timer') or not self._update_timer.is_alive():
            self._update_timer = rumps.Timer(self.update_countdowns, 1)
            self._update_timer.start()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filename='eyecare_app.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')
    try:
        app = EyeCareApp()
        app.run()
    except Exception as e:
        logging.exception("应用程序发生未捕获的异常")
        rumps.alert("应用程序错误", f"发生了一个错误: {e}\n请查看日志文件 eyecare_app.log 获取详细信息。")