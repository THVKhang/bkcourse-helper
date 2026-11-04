def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_paste_import_and_generate_schedule(client, sample_paste):
    r = client.post(
        "/imports/paste",
        json={"student_code": "2300001", "term_code": "252", "raw_text": sample_paste},
    )
    assert r.status_code == 200, r.text
    data = r.json()
    subject_ids = {s["subject_id"] for s in data["sections"]}
    assert {"CO3117", "CO3001"} <= subject_ids
    assert len(data["sections"]) == 4

    r = client.post(
        "/schedule/generate",
        json={
            "student_code": "2300001",
            "term_code": "252",
            "subject_ids": ["CO3117", "CO3001"],
        },
    )
    assert r.status_code == 200, r.text
    options = r.json()["options"]
    assert options, "expected at least one schedule option"
    for opt in options:
        scheduled = {it["subject_id"] for it in opt["items"]}
        assert scheduled == {"CO3117", "CO3001"}
        # CO3117 A01 is on Friday periods 8-9, so CO3001 must pick L01 (Monday)
        codes = {(it["subject_id"], it["section_code"]) for it in opt["items"]}
        assert ("CO3001", "L02") not in codes or ("CO3117", "A01") not in codes


def test_guest_login_and_me(client):
    r = client.post("/auth/guest")
    assert r.status_code == 200, r.text
    token = r.json()["token"]
    r = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200, r.text


def test_invalid_token_rejected(client):
    r = client.get("/auth/me", headers={"Authorization": "Bearer not-a-token"})
    assert r.status_code == 401
