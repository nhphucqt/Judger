#include <bits/stdc++.h>
#define tfi "bluehouse.inp"
#define tfo "bluehouse.out"
#define tfa "bluehouse.ans"
#define MAXLEN 1000000

using namespace std;

FILE    *themis_p_in,     // problem's input
        *themis_p_out,    // problem's output
        *themis_t_out,    // tested program's output
        *themis_t_src,    // tested program's source
        *themis_score,    // score for the program, for challenge problems
        *themis_u_info,   // additional info - psetter only
        *themis_p_info;   // additional info - psetter and solution's owner

void themis_init(const char*, const char*);
void local_init(const char*, const char*, const char*);
void read_in(const char*, ...);
void read_out(const char*, ...);
void read_ans(const char*, ...);
void message(const char*, ...);
void result(int);
void get_in(char*);
void get_out(char*);
void get_ans(char*);

//--------------------------------------------------------------------
#define maxn 50001
#define maxm 200001

typedef pair<int,int> II;

int n, m, deg[maxn];
vector<int> g[maxn];
II e[maxm];

int s[maxn], st[maxn], cl[maxn], cur[maxn], pe[maxn], pd[maxn];
int slt=0, id=0, num[maxn], low[maxn], lt[maxn];
void dfs(int xp) {
    int sn=0,stn=0;
    s[++sn]=xp, cl[xp]=1, pe[xp]=pd[xp]=0;
    st[++stn]=xp;
    num[xp]=low[xp]=++id;
    while (sn) {
        int u=s[sn];
        if (cur[u]<deg[u]) {
            int i=g[u][cur[u]++];
            if (i!=pe[u]) {
                int v=(e[i].first==u) ? e[i].second : e[i].first;
                if (cl[v]==0) {
                    s[++sn]=v, cl[v]=1, pe[v]=i, pd[v]=u;
                    st[++stn]=v;
                    num[v]=low[v]=++id;
                } else low[u]=min(low[u],num[v]);
            }
        } else {
            int w=pd[u];
            if (w) low[w]=min(low[w],low[u]);
            if (num[u]==low[u]) {
                ++slt;
                int v;
                do {
                    v=st[stn--];
                    lt[v]=slt;
                    cl[v]=2;
                } while (u!=v);
            }
            --sn;
        }
    }
}


int main(){
	themis_init(tfi, tfo);
    //local_init(tfi, tfo, tfa);
    read_in("%d%d",&n,&m);
    for(int i=1;i<=m;i++) {
        int u, v; read_in("%d%d",&u,&v);
        e[i]=make_pair(u,v);
        g[u].push_back(i); deg[u]++;
        g[v].push_back(i); deg[v]++;
    }
    int kqa; read_ans("%d",&kqa);
    int kqo; read_out("%d",&kqo);
    if (kqa!=kqo) {
        message("Wrong answer (DA=%d, HS=%d) !\n0.0");
        return 0;
    }
    for(int i=1;i<=kqo;i++) {
        int u, v; read_out("%d%d",&u,&v);
        e[++m]=make_pair(u,v);
        g[u].push_back(m); deg[u]++;
        g[v].push_back(m); deg[v]++;
    }

    for(int i=1;i<=n;i++) cl[i]=cur[i]=0;
    id=0;
    for(int i=1;i<=n;i++) if (cl[i]==0) dfs(i);

    if (slt>1) {
        message("Not conected!\n0.0");
        return 0;
    }
    message("Correct!\n");
    result(1); //1 - AC; 0 - WA
    return 0;
}

char TestPath[1000], CurrPath[1000];
char fINP[1000], fOUT[1000], fANS[1000];

void themis_init(const char* inName, const char* outName){
    gets(TestPath);
    gets(CurrPath);

    sprintf(fINP, "%s/%s", TestPath, inName);
    sprintf(fANS, "%s/%s", TestPath, outName);
    sprintf(fOUT, "%s/%s", CurrPath, outName);

    themis_p_in     = fopen(fINP, "r");
    themis_p_out    = fopen(fANS, "r");
    themis_t_out    = fopen(fOUT, "r");
}

void local_init(const char* inName, const char* outName, const char* ansName){
    themis_p_in     = fopen(inName, "r");
    themis_p_out    = fopen(ansName, "r");
    themis_t_out    = fopen(outName, "r");
}

void read_in(const char * format, ...){
	va_list args;
	va_start (args, format);
	int res = vfscanf (themis_p_in, format, args);
	va_end (args);
	if(res == EOF){
        message("Input not enough!!!\n");
        result(0.0);
	}
}

void get_in(char* s) {
    fgets(s,MAXLEN,themis_p_in);
}

void read_ans(const char * format, ...){
	va_list args;
	va_start (args, format);
	int res = vfscanf (themis_p_out, format, args);
	va_end (args);
	if(res == EOF){
        message("Answer not enough!!!\n");
        result(0.0);
	}
}

void get_ans(char* s) {
    fgets(s,MAXLEN,themis_p_out);
}

void read_out(const char * format, ...){
	va_list args;
	va_start (args, format);
	int res = vfscanf (themis_t_out, format, args);
	va_end (args);
	if(res == EOF){
        message("Output not enough!!!\n");
        result(0.0);
	}
}

void get_out(char* s) {
    fgets(s,MAXLEN,themis_t_out);
}

void message(const char * format, ...){
	va_list args;
	va_start (args, format);
	vfprintf (stdout, format, args);
	va_end (args);
}

void result(int score){
	fprintf(stdout, "%.1lf\n", double(score));
	exit(0);
}
