def test_checking_checkbox_marks_complete_with_strikethrough(page, live_server):
    page.goto(live_server + "/")
    checkbox = page.locator(".todo-row[data-id='1'] .todo-checkbox")
    row = page.locator(".todo-row[data-id='1']")

    checkbox.check()

    page.wait_for_function(
        "document.querySelector(\".todo-row[data-id='1']\").classList.contains('completed')"
    )
    assert "completed" in row.get_attribute("class")


def test_completed_state_persists_after_reload(page, live_server):
    page.goto(live_server + "/")
    checkbox = page.locator(".todo-row[data-id='1'] .todo-checkbox")
    row = page.locator(".todo-row[data-id='1']")
    checkbox.check()
    page.wait_for_function(
        "document.querySelector(\".todo-row[data-id='1']\").classList.contains('completed')"
    )

    page.reload()

    reloaded_checkbox = page.locator(".todo-row[data-id='1'] .todo-checkbox")
    reloaded_row = page.locator(".todo-row[data-id='1']")
    assert reloaded_checkbox.is_checked()
    assert "completed" in reloaded_row.get_attribute("class")
