from string import Template

private_start_message = 'Привет! \n\n\nЭтот микро-бот создан для того, чтобы отсечь самые глупые спам-боты приходящие в чат, которые \
не в состоянии нажать на клавишу "Войти". Несмотря на то, что бот простейший - развитие продолжается.\
Скоро будут новые функции.\n\n\n\
Для того, чтобы установить бота:\n\
1. Добавьте бота в чат, где Вы можете назначать адинистраторов;\n\
2. Назначьте бота администратором.\n\
Если у Вас возникли какие-либо вопросы или проблемы \
в работе с ботом - напишите об этом в чате @askerchat'

welcome_message = Template('Привет, $first_name! Для того, чтобы войти нажми клавишу "Войти"')
