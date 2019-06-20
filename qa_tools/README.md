### QA Test DOC


#### Loading Test
```The aim is to build stats on a view or process performance. We should rarely run this during daytime, recommended time is midnight and midWeek.```

Tools that we use for load test:
- Locust.io https://docs.locust.io/en/stable/


How to run load test
- Create a test user

    ```
    Never use a real user account for load test.
    Ensure that you have an admin role, if you dont; please ask an admin to share a test user credentail with you and move to the next step.
    ```
    *For admin only*
    - hit the `qa/create_test_user/` route
    - you shall use the response to qa

- Update the the content of the `vars.env` file in the qa_tools.load_test app. Create an copy of `sample.env` if you do not have one. The content should look like this

```
LOGIN_URL=/user/login/
LOGOUT_URL=/user/logout/
RESERVATION_URL=/reservation/
AVAILABLE_FLIGHTS=/available_flights/
FLIGHT_CLASS=/flight_class/
EMAIL=
PASSWORD=
HOST=
```
- Run this  command to run an load test file (it's more confortale if you run this in the qa_tools directory). `locust -f <test_file> --host=<host> -c 1000 -r 100 --run-time 1h30m`

    keys:

        - c: the number of users that would be simulated
        - r: the number of user to have completed the steps in one second
        -run-time: how long the entire test should run (if you skip this, the test might run for even; we don't want that.)

- if you have the web component, then go to `http://localhost:8089/` to view the dashboard



*Request for support when you have a challenge or observe something strange.*



