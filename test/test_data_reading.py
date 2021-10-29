import pandas
import pytest
import hermes.stroke_regressor
import pandas as pd  # type: ignore
import numpy as np
import string
import random
from sklearn.preprocessing import MinMaxScaler, StandardScaler

random.seed = 0


def test_read_data():
    file_loc = '/tmp/simple.csv'
    with open(file_loc, 'w') as f:
        f.write('Name,Number,Double\nhalp me,7,22.8\nplease,69,13.37\n')
    simple = hermes.stroke_regressor.read_data(file_loc)
    assert simple.shape == (2, 3)
    assert simple.equals(pd.DataFrame({'Name': ['halp me', 'please'], 'Number': [7, 69], 'Double': [22.8, 13.37]}))


def test_read_data_2():
    name = np.random.uniform(0, 1000, 100)
    for i in range(100):
        file_loc = f'/tmp/test{name[i]}.csv'
        data = np.random.uniform(0, 1000, (100, 3))
        df = pd.DataFrame(data=data, columns=['Name', 'Number', 'Double'])
        df.to_csv   (file_loc, index=False)
        simple = hermes.stroke_regressor.read_data(file_loc)
        assert simple.shape == (100, 3)
        assert np.allclose(df.to_numpy(), simple.to_numpy())


def get_random_string(n):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=n))


def test_one_hot_encoded():
    leng = np.reshape(list(map(get_random_string, range(1, 3*4+1))), (4, 3))
    mx = np.array(np.random.rand(4, 3)*3, dtype=np.int64)
    data = []
    ans = np.zeros((4, 9), dtype=np.int64)
    for (i, row) in enumerate(mx):
        data.append([])
        for (j, val) in enumerate(row):
            data[-1].append(leng[j][val])
            ans[i][3*j + val] = 1
    cols = []
    for (i, name) in enumerate(leng[3]):
        cols.append(f"{name}_{leng[i][0]}")
        cols.append(f"{name}_{leng[i][1]}")
        cols.append(f"{name}_{leng[i][2]}")
    df_q = pandas.DataFrame(data=data, columns=leng[3])
    df_ans = pandas.DataFrame(data=ans, columns=cols)
    df_ans = df_ans.loc[:, (df_ans != 0).any(axis=0)]
    df_check = hermes.stroke_regressor.one_hot(df_q)
    df_ans = df_ans.reindex(sorted(df_ans.columns), axis=1)
    df_check = df_check.reindex(sorted(df_check.columns), axis=1)
    assert np.allclose(df_ans.to_numpy(), df_check.to_numpy())


def test_normalize_minmax():
    data = np.array([[-1, 2], [-0.5, 6], [0, 10], [1, 18]])
    ans = (data - np.nanmin(data, axis=0))/(np.nanmax(data, axis=0) - np.nanmin(data, axis=0))
    check = hermes.stroke_regressor.normalize(pd.DataFrame(data))
    assert np.allclose(ans, check)

def test_normalize_standard():
    data = np.random.rand(7, 12)
    ans = (data - data.mean(axis=0)) / data.std(axis=0)
    check = hermes.stroke_regressor.normalize(data, type='standard')
    assert np.allclose(ans, check)
