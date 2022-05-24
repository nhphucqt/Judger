#include <bits/stdc++.h>

using namespace std;

const string name = "PARTITION";
ifstream inp, ans, out;

const int N = 5e6+7;
int n, k, a[N];
pair<int,int> seq[N];
int out_x, out_y, ans_x, ans_y;
int cnt[N];

bool result(string msg, bool ok) {
    cout << msg << '\n';
    if (ok) cout << "1.0";
    else cout << "0.0";

    inp.close();
    ans.close();
    out.close();

    exit(0);
}

void check_x_y() {
    out >> out_x >> out_y;
    ans >> ans_x >> ans_y;

    if (out_x != ans_x || out_y != ans_y)
	result("Khac x, y", false);

//    if (out_y - out_x != ans_y - ans_x)
//	result("khac y - x", 0);

//    if (out_x < ans_x)
//	result("out_x < ans_x", 0);
}

void check_valid_subsequences() {
    inp >> n >> k;
    for (int i = 1; i <= n; ++i) {
        inp >> a[i];
    }

    //
    {
        int cnt = 0;
        while (out >> seq[cnt+1].first >> seq[cnt+1].second) {
            if (++cnt > k) result("so luong doan nhieu hon k", 0);
        }
        if (cnt != k) result("so luong doan khac k", 0);
    }

    //
    for (int i = 1; i <= k; ++i) {
        if (seq[i].first > seq[i].second)
            result("doan khong thoa man (x > y)", 0);
        if (seq[i].first < 1 || seq[i].second > n)
            result("gioi han doan nam ngoai [1, n]", 0);
        cnt[seq[i].first]++;
        cnt[seq[i].second+1]--;
    }
    for (int i = 1; i <= n; ++i) {
        cnt[i] += cnt[i-1];
        if (cnt[i] != 1) result("phan tu khong nam trong hoac nam tren nhieu doan con", 0);
    }

    //
    bool found = false;
    for (int i = 1; i <= k; ++i) {
        int num = 0;
        for (int j = seq[i].first; j <= seq[i].second; ++j) {
            num += out_x <= a[j] && a[j] <= out_y ? 1 : -1;
        }
        if (num <= 0)
            result("so luong nam trong <= so luong nam ngoai", 0);
        if (i < k) {
            found |= seq[i].second + 1 != seq[i+1].first;
        }
    }

    if (found)
        result("ket qua dung, in doan khong theo thu tu", 1);
    result("ket qua dung, in doan theo thu tu", 1);
}

int main() {
    string testcase_path, output_path;
    cin >> testcase_path >> output_path;

    inp.open(testcase_path + name + ".inp");
    ans.open(testcase_path + name + ".out");
    out.open(output_path + name + ".out");

    inp.tie(nullptr)->sync_with_stdio(false);
    ans.tie(nullptr)->sync_with_stdio(false);
    out.tie(nullptr)->sync_with_stdio(false);


    check_x_y();
    check_valid_subsequences();

    cerr << "here\n";

    return 0;
}
