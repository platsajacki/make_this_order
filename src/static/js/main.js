/**
 * Основной сценарий работы с заказами на сервере.
 *
 * Этот скрипт загружает столы и блюда, позволяет добавлять новые позиции в заказ,
 * создавать заказы, удалять заказы, обновлять статус заказов и выводить информацию о выручке за смену.
 * Также предоставляет возможность поиска и фильтрации заказов по различным параметрам.
 *
 * Основные действия:
 * 1. Загрузка столов (`loadTables`) и блюд (`loadDishes`), которые отображаются в селекторах.
 * 2. Добавление новой позиции в заказ с заполнением доступных блюд.
 * 3. Создание нового заказа с выбранными блюдами и количеством.
 * 4. Удаление заказов.
 * 5. Обновление статуса заказа.
 * 6. Загрузка информации о выручке за смену.
 * 7. Поиск и фильтрация заказов.
 *
 * @module main
 */

const tablesApiUrl = '/api/v1/tables/' // URL для получения столов
const dishesApiUrl = '/api/v1/dishes/' // URL для получения блюд
const createOrderApiUrl = '/api/v1/orders/' // URL для создания заказа

/**
 * Загружает данные о столах, блюдах и выручке за смену при загрузке страницы.
 */
document.addEventListener('DOMContentLoaded', async function () {
    await loadTables() // Загружаем столы
    await loadDishes() // Загружаем блюда
    await loadShiftRevenue() // Загружаем выручку за смену
})

/**
 * Загружает список доступных столов с сервера и заполняет элемент выбора стола.
 */
async function loadTables() {
    const response = await fetch(tablesApiUrl)
    const data = await response.json()
    const tableSelect = document.getElementById('table_create')

    tableSelect.innerHTML = data.map(table =>
        `<option value="${table.id}">${table.number}</option>`
    ).join('')
}

/**
 * Загружает список доступных блюд с сервера и заполняет все элементы select для выбора блюда.
 */
async function loadDishes() {
    const response = await fetch(dishesApiUrl)
    const data = await response.json()
    const dishSelects = document.querySelectorAll('.dish-select')

    dishSelects.forEach(select => {
        if (!select.children.length) {
            select.innerHTML = data.map(dish =>
                `<option value="${dish.id}">${dish.name}</option>`
            ).join('')
        }
    })
}

/**
 * Обработчик события для добавления нового элемента в заказ.
 * Создает новый блок с полями для выбора блюда и количества.
 */
document.getElementById('add-item').addEventListener('click', function () {
    const orderItems = document.getElementById('order-items')
    const newItem = document.createElement('div')
    newItem.classList.add('order-item')
    newItem.innerHTML = `
        <label>Название блюда</label>
        <select name="dish_name[]" class="dish-select" required></select>
        <label>Количество</label>
        <input type="number" name="quantity[]" required min="1">
        <button type="button" onclick="removeItem(this)">Удалить</button>
    `
    orderItems.appendChild(newItem)
    loadDishes()  // Заполняем select-ы блюдами
})

/**
 * Удаляет элемент из заказа при нажатии на кнопку "Удалить".
 *
 * @param {HTMLElement} button Кнопка "Удалить", вызвавшая функцию.
 */
function removeItem(button) {
    button.parentElement.remove()
}

/**
 * Обработчик события для отправки формы создания заказа.
 * Собирает данные о заказе и отправляет их на сервер для создания.
 */
document.getElementById('create-order-form').addEventListener('submit', async function (e) {
    e.preventDefault()

    const tableNumber = document.getElementById('table_create').value
    const dishNames = Array.from(document.querySelectorAll('select[name="dish_name[]"]')).map(select => select.value)
    const quantities = Array.from(document.querySelectorAll('input[name="quantity[]"]')).map(input => input.value)

    const uniqueDishes = new Set(dishNames);
    if (uniqueDishes.size !== dishNames.length) {
        alert('Вы не можете выбрать одинаковые блюда при создании заказа.\nПожалуйста, изменяйте количество.')
        return
    }

    const orderData = {
        table: tableNumber,
        items: dishNames.map((dishId, index) => ({
            dish: dishId,
            quantity: quantities[index],
        })),
    }

    const response = await fetch(createOrderApiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify(orderData),
    })

    if (response.ok) {
        alert('Заказ создан успешно')
        location.reload()
    } else if (response.status === 400) {
        const errorData = await response.json()
        alert(JSON.stringify(errorData, null, 2))
    } else {
        alert('Ошибка при создании заказа')
    }
})

/**
 * Загружает список заказов с сервера с учетом фильтрации по параметрам.
 */
async function getOrders() {
    const tableNumber = document.getElementById('table').value
    const status = document.getElementById('status').value
    const orderId = document.getElementById('order_id').value
    const queryParams = new URLSearchParams()

    if (tableNumber) queryParams.append('table', tableNumber)
    if (status) queryParams.append('status', status)
    if (orderId) queryParams.append('id', orderId)

    const url = `/api/v1/orders/?${queryParams.toString()}`
    const response = await fetch(url)
    const orders = await response.json()

    const tbody = document.getElementById('order-table-body')
    tbody.innerHTML = ''

    orders.forEach(order => {
        const row = document.createElement('tr')
        row.innerHTML = `
            <td>${order.id}</td>
            <td>${order.table.number}</td>
            <td>${order.items.map(item => `${item.dish.name} (${item.quantity})`).join(', ')}</td>
            <td>${order.total_price}</td>
            <td><button onclick="deleteOrder(${order.id})">Удалить</button></td>
            <td>
                <select onchange="updateOrderStatus(${order.id}, this)">
                    <option value="pending" ${order.status === 'pending' ? 'selected' : ''}>В ожидании</option>
                    <option value="ready" ${order.status === 'ready' ? 'selected' : ''}>Готово</option>
                    <option value="paid" ${order.status === 'paid' ? 'selected' : ''}>Оплачено</option>
                </select>
            </td>
        `
        tbody.appendChild(row)
    })
}

/**
 * Удаляет заказ по его ID.
 *
 * @param {number} orderId Идентификатор заказа.
 */
async function deleteOrder(orderId) {
    if (confirm('Вы уверены, что хотите удалить этот заказ?')) {
        const url = `/api/v1/orders/${orderId}/`
        const response = await fetch(url, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
        })

        if (response.status === 204) {
            alert('Заказ удален')
            getOrders()
        } else {
            alert('Ошибка при удалении заказа')
        }
    }
}

/**
 * Обновляет статус заказа по его ID.
 *
 * @param {number} orderId Идентификатор заказа.
 * @param {HTMLElement} selectElement Элемент select с новым статусом.
 */
async function updateOrderStatus(orderId, selectElement) {
    const status = selectElement.value
    const url = `/api/v1/orders/${orderId}/`
    const response = await fetch(url, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({ status: status }),
    })

    if (response.ok) {
        alert('Статус обновлен')
        getOrders()
        loadShiftRevenue()
    } else {
        alert('Ошибка при обновлении статуса')
    }
}

/**
 * Загружает информацию о выручке за смену.
 */
async function loadShiftRevenue() {
    try {
        const response = await fetch('/api/v1/shift-revenue/')
        const data = await response.json()
        const revenueElement = document.getElementById('revenue-amount')
        if (data.total_revenue !== undefined) {
            revenueElement.textContent = `${data.total_revenue} ₽`
        } else {
            revenueElement.textContent = 'Не удалось получить данные'
        }
    } catch (error) {
        console.error('Ошибка при загрузке выручки за смену:', error)
        document.getElementById('revenue-amount').textContent = 'Ошибка загрузки'
    }
}

/**
 * Загружает заказы при загрузке страницы.
 */
window.onload = getOrders

/**
 * Обработчик события для отправки формы поиска заказов.
 * Загружает заказы с учетом фильтров.
 */
document.getElementById('search-form').addEventListener('submit', function (e) {
    e.preventDefault()
    getOrders()
})
