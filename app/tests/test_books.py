def get_headers(auth_token):
    _headers = {"Authorization": f"Bearer {auth_token}"}
    return _headers


def test_create_user(test_client, credentials_payload):
    response = test_client.post("/auth/signup", data=credentials_payload)
    assert response.status_code == 200


def test_create_book(test_client, biblion_payload, credentials_payload):
    response = test_client.post("/auth/signup", data=credentials_payload)
    assert response.status_code == 200

    response = test_client.post("/auth/token", data=credentials_payload)
    assert response.status_code == 200

    headers = get_headers(response.json()["access_token"])
    response = test_client.post("/biblion/", data=biblion_payload, headers=headers)
    assert response.status_code == 200
    assert "id" in response.json()


def test_get_book(test_client, credentials_payload, biblion_payload):
    response = test_client.post("/auth/signup", data=credentials_payload)
    assert response.status_code == 200

    response = test_client.post("/auth/token", data=credentials_payload)
    assert response.status_code == 200

    headers = get_headers(response.json()["access_token"])

    response = test_client.post("/biblion/", data=biblion_payload, headers=headers)
    assert response.status_code == 200
    assert "id" in response.json()

    biblion_id = response.json()["id"]
    response = test_client.get(f"/biblion/{biblion_id}", headers=headers)
    assert response.status_code == 200
    assert "id" in response.json()


def test_get_all_books(test_client, credentials_payload, biblion_payload):
    response = test_client.post("/auth/signup", data=credentials_payload)
    assert response.status_code == 200

    response = test_client.post("/auth/token", data=credentials_payload)
    assert response.status_code == 200

    headers = get_headers(response.json()["access_token"])

    response = test_client.post("/biblion/", data=biblion_payload, headers=headers)
    assert response.status_code == 200
    assert "id" in response.json()

    response = test_client.get("/biblion/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0
    assert "id" in response.json()[0]


def test_update_book(test_client, updated_biblion_payload, credentials_payload, biblion_payload):
    response = test_client.post("/auth/signup", data=credentials_payload)
    assert response.status_code == 200

    response = test_client.post("/auth/token", data=credentials_payload)
    assert response.status_code == 200

    headers = get_headers(response.json()["access_token"])

    response = test_client.post("/biblion/", data=biblion_payload, headers=headers)
    assert response.status_code == 200
    assert "id" in response.json()

    biblion_id = response.json()["id"]
    response = test_client.put(f"/biblion/{biblion_id}", data=updated_biblion_payload, headers=headers)
    assert response.status_code == 200

    updated_biblion_payload["id"] = biblion_id
    assert response.json() == updated_biblion_payload


def test_delete_book(test_client, credentials_payload, biblion_payload):
    response = test_client.post("/auth/signup", data=credentials_payload)
    assert response.status_code == 200

    response = test_client.post("/auth/token", data=credentials_payload)
    assert response.status_code == 200

    headers = get_headers(response.json()["access_token"])

    response = test_client.post("/biblion/", data=biblion_payload, headers=headers)
    assert response.status_code == 200
    assert "id" in response.json()

    biblion_id = response.json()["id"]
    response = test_client.delete(f"/biblion/{biblion_id}", headers=headers)
    assert response.status_code == 200

    response = test_client.get(f"/biblion/{biblion_id}", headers=headers)
    assert response.status_code == 404
