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


def test_failed_patch_reverts_checkbox_and_shows_error(page, live_server):
    page.route(
        "**/todos/1",
        lambda route: route.fulfill(status=500, body="server error"),
    )
    page.goto(live_server + "/")
    checkbox = page.locator(".todo-row[data-id='1'] .todo-checkbox")
    row = page.locator(".todo-row[data-id='1']")
    error = page.locator(".todo-row[data-id='1'] .todo-error")

    checkbox.check()

    page.wait_for_function(
        "document.querySelector(\".todo-row[data-id='1'] .todo-error\").textContent.length > 0"
    )
    assert not checkbox.is_checked()
    assert "completed" not in row.get_attribute("class")
    assert error.text_content() != ""
