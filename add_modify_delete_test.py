import requests
import json
import pytest
from helpers import *
from service_runner import Alaska, run_alaska_service


@pytest.fixture
def alaska():
    alaska = Alaska()
    p = run_alaska_service(alaska.get_port())
    yield alaska
    p.kill()


@pytest.fixture
def bears():
    return Bears()


def test_info(alaska):
    r = requests.get(alaska.get_url() + "/info")
    assert r.ok


def test_add_new_bear(alaska, bears):
    r = requests.get(alaska.get_default())
    assert r.ok
    assert len(r.json()) == 0

    assert requests.post(alaska.get_default(),
                         data=json.dumps(bears.get_Semen())).ok

    res = requests.get(alaska.get_default())
    bears_list = res.json()
    assert len(bears_list) == 1
    assert bears_eq(bears_list[0], bears.get_Semen())


def test_get_special_bear(alaska, bears):
    assert requests.post(alaska.get_default(),
                         data=json.dumps(bears.get_Semen())).ok
    assert requests.post(alaska.get_default(),
                         data=json.dumps(bears.get_Boris())).ok

    res = requests.get(alaska.get_default())
    bears_list = res.json()
    assert len(bears_list) == 2

    for bear in bears_list:
        r = requests.get(alaska.get_default()+"/"+str(bear['bear_id']))
        assert r.ok
        assert bears_eq(bear, r.json())


def test_modify_bear(alaska, bears):
    my_bear = bears.get_Semen()
    assert requests.post(alaska.get_default(), data=json.dumps(my_bear)).ok

    res = requests.get(alaska.get_default())
    bears_list_beafore_update = res.json()
    assert res.ok
    assert len(bears_list_beafore_update) == 1

    bear_id = bears_list_beafore_update[0]['bear_id']
    my_bear['bear_name'] = str("ex. ") + my_bear['bear_name']

    assert requests.put(alaska.get_default() + "/" +
                        str(bear_id), data=json.dumps(my_bear)).ok

    res = requests.get(alaska.get_default())
    bears_list_after_update = res.json()
    assert len(bears_list_after_update) == 1
    assert bears_eq(bears_list_after_update[0], my_bear)


def test_delete_bear(alaska, bears):
    assert requests.post(alaska.get_default(),
                         data=json.dumps(bears.get_Semen())).ok
    assert requests.post(alaska.get_default(),
                         data=json.dumps(bears.get_Boris())).ok

    res = requests.get(alaska.get_default())
    bears_list = res.json()

    assert len(bears_list) == 2
    bear_for_delete = bears_list[0]
    bear_for_leave = bears_list[1]
    assert requests.delete(alaska.get_default() + "/" +
                           str(bear_for_delete['bear_id'])).ok

    res = requests.get(alaska.get_default())
    bears_list = res.json()
    assert len(bears_list) == 1
    assert bears_eq(bears_list[0], bear_for_leave)


def test_delete_all_bears(alaska, bears):
    assert requests.post(alaska.get_default(),
                         data=json.dumps(bears.get_Semen())).ok
    assert requests.post(alaska.get_default(),
                         data=json.dumps(bears.get_Boris())).ok

    assert requests.delete(alaska.get_default()).ok

    res = requests.get(alaska.get_default())
    bears_list = res.json()
    assert len(bears_list) == 0


def test_update_unexisting_bear(alaska, bears):
    assert requests.post(alaska.get_default(),
                         data=json.dumps(bears.get_Semen())).ok
    assert requests.post(alaska.get_default(),
                         data=json.dumps(bears.get_Boris())).ok

    res = requests.get(alaska.get_default())
    bears_list_beafore_update = res.json()
    assert res.ok
    assert len(bears_list_beafore_update) == 2

    new_bear = bears.get_Semen()
    new_bear['bear_name'] = new_bear['bear_name'] + str(" Sun")

    wrong_id = bears_list_beafore_update[0]['bear_id'] + \
        bears_list_beafore_update[1]['bear_id']
    assert not requests.put(alaska.get_default()+"/" +
                            str(wrong_id), data=new_bear).ok

    res = requests.get(alaska.get_default())
    bears_list_after_update = res.json()
    assert len(bears_list_after_update) == 2

    bears_dict_after_update = bears_to_dict(bears_list_after_update)

    for bear in bears_list_beafore_update:
        assert bears_eq(bears_dict_after_update[bear['bear_id']], bear)