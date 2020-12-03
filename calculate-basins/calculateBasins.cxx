#include <algorithm>
#include <iostream>
#include <functional>
#include <map>
#include <vector>


using namespace std;


vector<int> calculateBasins(vector<vector<int>> grid) {
    const vector<vector<int>> kDirs = { { -1, 0 }, { 1, 0 }, { 0, -1 }, { 0, 1 } };
    const int Y = grid.size(), X = grid[0].size();
    
    vector<vector<pair<int, int>>> memo(Y, vector<pair<int, int>>(X, { -1, -1 }));
    function<void(int&,int&)> dfs = [&] (int &y, int &x) {
        if (memo[y][x].first != -1) return;
        int mih = grid[y][x], mi = -1;
        for (int i = 0; i < int(kDirs.size()); ++i) {
            int ny = y + kDirs[i][0], nx = x + kDirs[i][1];
            if (ny >= 0 && ny < Y && nx >=0 && nx < X && grid[ny][nx] < mih) {
                mi = i;
                mih = grid[ny][nx];
            }
        }
        if (mi > -1) {
            int cy = y, cx = x;
            y += kDirs[mi][0];
            x += kDirs[mi][1];
            if (memo[y][x].first == -1) {
                dfs(y, x);
            } else {
                int ty = memo[y][x].first;
                x = memo[y][x].second;
                y = ty;
            }
            memo[cy][cx] = { y, x };        
        } else {
            memo[y][x] = { y, x };
        }
    };
    
    for (int y = 0; y < Y; ++y) {
        for (int x = 0; x < X; ++x) {
            int tx = x, ty = y;
            dfs(ty, tx);
        }
    }
    map<pair<int, int>, int> basins;
    for (int y = 0; y < Y; ++y) {
        for (int x = 0; x < X; ++x) {
            ++basins[memo[y][x]];
            //cout << memo[y][x].first * X + memo[y][x].second << "|" << grid[y][x] << "\t";
            cout << memo[y][x].first * X + memo[y][x].second << "\t";
        }
        cout << endl;
    }
    
    vector<int> res;
    for (auto &b: basins) res.push_back(b.second);
    sort(res.begin(), res.end(), [] (int l, int r) { return l > r; });
    return res;
}


int main() {
    int n;
    cin >> n;

    vector<vector<int>> grid(n, vector<int>(n));
    for (int i = 0; i < n; ++i) for (int j = 0; j < n; ++j) cin >> grid[i][j];

    calculateBasins(grid);
}

// Local Variables:
// compile-command: "g++ -x c++ -std=gnu++17 -O2 task.cxx && \
//     time ./a.out <grid.txt >output_cpp.txt"
// End:
