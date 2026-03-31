def test_create_and_get_dog(client):
    # Create
    r = client.post("/dogs", json={"name": "Milo", "age_years": 3})
    assert r.status_code == 201
    data = r.json()
    assert "id" in data
    assert data["name"] == "Milo"
    dog_id = data["id"]

    # Get by id
    r2 = client.get(f"/dogs/{dog_id}")
    assert r2.status_code == 200
    data2 = r2.json()
    assert data2["id"] == dog_id
    assert data2["name"] == "Milo"


def test_list_dogs(client):
    client.post("/dogs", json={"name": "A"})
    client.post("/dogs", json={"name": "B"})
    r = client.get("/dogs")
    assert r.status_code == 200
    dogs = r.json()
    assert len(dogs) == 2


def test_patch_updates_only_name(client):
    r = client.post("/dogs", json={"name": "OldName", "age_years": 5, "breed": "Husky"})
    dog = r.json()
    dog_id = dog["id"]

    # Patch only the name
    r2 = client.patch(f"/dogs/{dog_id}", json={"name": "NewName"})
    assert r2.status_code == 200
    updated = r2.json()
    assert updated["name"] == "NewName"
    # These should remain unchanged
    assert updated["age_years"] == 5
    assert updated["breed"] == "Husky"


def test_delete_dog(client):
    r = client.post("/dogs", json={"name": "ToDelete"})
    dog_id = r.json()["id"]

    d = client.delete(f"/dogs/{dog_id}")
    assert d.status_code == 204

    g = client.get(f"/dogs/{dog_id}")
    assert g.status_code == 404
