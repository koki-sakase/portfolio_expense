# ==========================================
#  家計簿の作成
# 以前個人的に作成したものをポートフォリオ用に新たに作製したデモ版となります。
# 以下の項目を理由にこの家計簿は作成しました。
# ・一人暮らしに伴い家計簿をつける必要があったため
# ・pc、スマホ両方で使用できるようにしたかったが見える範囲での家計簿アプリは有料であったため
# ・pythonの勉強も兼ねて作成したかったため

# 実際はGoogleDriveのsecret.jsonを用いて実際にスプレッドシートのファイルに書き込むよう設計しましたが、こちらは非公開とさせていただいているため、このようにデモ版を作製した次第です。

# 使用している言語はpythonで、フレームワークはstreamlitを使用しています。
# 使用している環境はvscodeです。

# フローチャートを別ファイル(mdファイル)に記載しています。以降現れるstepとはフローチャートに記載されている数字と対応しています。
# ==========================================

# ==========================================
# 1.アプリの起動またはブラウザの更新
# 2. UI基本設定

# streamlitを使用してアプリを作成しています。
# streamlitはpythonで簡単にwebアプリを作成できるフレームワークであり、UIの基本設定も簡単に行うことができます。
# このstepではUIの基本設定と必要なライブラリを書いています。
# コンテンツは中央に配置するレイアウトにしています。
# ==========================================

import streamlit as st
import pandas as pd # step4で追加
from datetime import datetime
import os # step4で追加

st.set_page_config(page_title="家計簿アプリ",layout="centered")

st.title("家計簿アプリ")

# ==========================================
# 3.メモリ領域にデータ(df)が存在しているか

# streamlitではユーザーごとにメモリの保存ができます。st.session_stateを使用することで、ユーザーごとにデータを保存することができます。
# このコードではdfという変数でデータを格納・抽出しております。
# 当stepでは、メモリ領域にデータが存在しているかを確認し、存在していない場合は新たにデータを作成する処理を行っています。
# 以前作成した家計簿ではjsonファイルを入手し、個人のgoogleアカウントにおけるgoogle driveおよびgoogle spread sheetを使用してデータの保存・抽出を行っていましたが、今回はポートフォリオ用に作成しているため、このファイルと同フォルダ内にcsvファイルを作成し、データの保存・抽出を行うようにしています。
# あくまでこのcsvファイルはデータの保存・抽出を行うためのものであり、ユーザーが直接操作するものではないため、ユーザーがこのcsvファイルを操作することは想定しておらず、またこのpythonファイルによる書き込みはできないようにしております。
# ==========================================

if "df" not in st.session_state:
    # st.write("データフレームが存在しません。")
    # ↑のコードはデバッグ用のコードであり、実際のアプリでは表示しないようにしています。step4への移動に伴いコメントアウトしました

    # ==========================================
    # 4.ローカルのdata.csvをロード

    # ローカルのdata.csvをロードしています。「DATA_FILE」にcsvデータの指定のみをしており、データの有無の判定はstep6, 7で行っております。
    # ==========================================

    DATA_FILE = "data.csv"

    # ==========================================
    # 6. CSVから履歴・設定を読み込み、メモリ領域へ格納

    # ローカルにdata.csvが存在している場合は、csvを読み込み、メモリ領域へ格納する処理を行っています。
    # また、step7のコメントにある大分類、詳細項目における項目の初期設定をしています。
    # ==========================================
    
    if os.path.exists(DATA_FILE):
        st.session_state.df = pd.read_csv(DATA_FILE)

        # ==========================================
        # step7のコメントにあるアカウント、大分類、詳細項目における項目の初期設定をしています。

        # ==========================================

        if 'accounts_init' not in st.session_state:
            st.session_state.accounts_init = {'口座': 1000000, '現金': 30000, 'クレジットカード':-10000}

        base_majors = ["食費", "光熱費"]
        saved_majors = st.session_state.df['大分類'].dropna().unique().tolist() if not st.session_state.df.empty else []
        st.session_state.known_majors = list(set(base_majors + saved_majors))

        base_details = ["Amazon", "マックスバリュ"]
        saved_details = st.session_state.df['詳細項目'].dropna().unique().tolist() if not st.session_state.df.empty else []
        st.session_state.known_details = list(set(base_details + saved_details))
    
    # ==========================================
    # 7. 空のdf・初期アカウント・基本リストを生成し、メモリ領域へ格納

    # ローカルにdata.csvが存在していない場合は、空のデータフレームを生成し、メモリ領域へ格納する処理を行っています。
    # '日付', 'アカウント','大分類', '詳細項目', '品目', '単価', '数量', '税率', '金額', '種別'とありますが、対応する項目は以下の通りです。
    # ・日付：支出および収入が発生した日付
    # ・アカウント：支出および収入が発生したアカウント（例：現金、クレジットカードなど）
    # ・大分類：支出および収入の大分類（例：食費、交通費など）
    # ・詳細項目：支出および収入の詳細項目（例：店名など）
    # ・品目：支出および収入の品目（例：米、野菜など）
    # ・単価：支出および収入の単価
    # ・数量：支出および収入の数量
    # ・税率：支出および収入の税率
    # ・金額：支出および収入の金額
    # ・種別：支出および収入の種別（例：食費、交通費など）

    # アカウントの初期値について、クレジットカードはマイナス表記となっておりますが、これは現在の未払い分を表しており、支払い日に振替として口座からクレジットカードに資金移動することによって、クレジットカードの支払いを表しております。
    # ==========================================

    else:
        headers=['日付', 'アカウント','大分類', '詳細項目', '品目', '単価', '数量', '税区分', '税率', '金額', '種別']
        st.session_state.df = pd.DataFrame(columns=headers)
        st.session_state.accounts_init = {'口座': 1000000, '現金': 30000, 'クレジットカード':-10000}
        st.session_state.known_majors = ["食費", "光熱費"]
        st.session_state.known_details = ["Amazon", "マックスバリュ"]

# ==========================================
# 5. 既存のメモリ領域のデータを維持
# データフレームにデータが格納されていた場合に、そのデータを維持する項目です。
# そのままpathを行っています。
# ==========================================

else:
    # st.write("データフレームが存在しています。")
    # ↑はデバック用のためコメントアウト
    pass
    
# ==========================================
# 8. 残高の自動計算
# 残高の計算を自動で行っています。
# 支出を選択した場合は入力した金額を減算、収入を選択した場合には加算、振替を選択した場合には出金元を減算、入金先を加算しております。
# ==========================================

balances = st.session_state.accounts_init.copy()

for acc in st.session_state.df['アカウント'].dropna().unique():
    if acc not in balances and ' → ' not in acc:
        balances[acc] = 0

for _, row in st.session_state.df.iterrows():
    try:
        amt = int(str(row['金額']).replace(',', ''))
    except ValueError:
        continue

    acc = str(row['アカウント'])
    ctype = str(row['種別'])

    if ctype == '支出':
        if acc in balances:
            balances[acc] -= amt
    elif ctype == '収入':
        if acc in balances:
            balances[acc] += amt

    elif ctype == '振替':
        if ' → ' in acc:
            parts = acc.split(' → ')
            if len(parts) == 2:
                from_acc , to_acc = parts[0], parts[1]
            if from_acc in balances:
                balances[from_acc] -= amt
            if to_acc in balances:
                balances[to_acc] += amt

# ==========================================
# 9. メイン画面への描画およびタブ描画

# 残高などを示すメイン描画や、家計簿の新規入力を行うサイドバー描画を行っています。
# メイン描画については、一行3アカウントまでを表示させております。
# また、タブ描画については、タブを3つ設定し、支出の分析、履歴の一覧、設定・データ管理としています。
# ==========================================

st.markdown("### 現在の残高")
acc_names = list(balances.keys())

for i in range(0, len(acc_names), 3):
    cols = st.columns(3)
    for j in range(3):
        if i+j < len(acc_names):
            acc = acc_names[i+j]
            cols[j].metric(acc, f"{balances[acc]:,}")
st.markdown("---")

st.sidebar.header("新規入力")

tab1, tab2, tab3 = st.tabs(["支出の分析" , "履歴の一覧" , "設定・データ管理"])

# ==========================================
# 10. 新規データの入力フォーム処理

# サイドバーにおける新規データの入力を行っております。日付、アカウント、種別、大分類、詳細項目、品目、単価、数量、税区分、税率を入力するフォームです。大分類、詳細項目以外は決まったリストから選択するselectboxやradio、あるいは手入力のtext_inputやnumber_inputを使っております。大分類、詳細項目は決まったリストに加えて新規入力の欄を追加しており、新規入力を選択した際、text_inputでテキストを入力することでデータフレームに大分類、詳細項目の欄が追加される、という仕様になっております。

# ==========================================

with st.sidebar:
    st.markdown("### データ入力")
    date = st.date_input("日付")
    type_ = st.selectbox("種別", ["支出", "収入", "振替"])

    if type_ in ["支出", "収入"]:
        account = st.selectbox("アカウント", list(balances.keys()))
        category_choice = st.selectbox("大分類", st.session_state.known_majors+["(新規入力)"])
        if category_choice == "(新規入力)":
            category = st.text_input("新しい大分類を入力")
        else :
            category = category_choice
    
        sub_choice = st.selectbox("詳細項目", st.session_state.known_details+["(新規入力)"])
        if sub_choice == "(新規入力)":
            subcategory = st.text_input("新しい詳細項目を入力")
        else:
            subcategory = sub_choice

        item =st.text_input("品目")

        price = st.number_input("単価", min_value=0, step = 1)
        quantity = st.number_input("数量", min_value=0, step=1)
        tax_type = st.radio("税区分", ["税抜", "税込"], horizontal=True)
        tax_rate = st.radio("税率", ["0%", "8%", "10%"], horizontal=True)

        rate_num = float(tax_rate.replace("%",""))/100

        base_amount = price * quantity
        if tax_type == "税抜":
            total_amount = int(base_amount * (1 + rate_num))

        else :
            total_amount = base_amount

        st.sidebar.write(f"**計算結果 (税込): {total_amount:,} 円**")

        submit_button = st.button("データ入力", type="primary")

        if submit_button:
        
            new_data = pd.DataFrame([{
                '日付': date,
                '種別': type_,
                'アカウント': account,
                '大分類': category,
                '詳細項目': subcategory,
                '品目': item,
                '単価': price,
                '数量': quantity,
                '税区分': tax_type,
                '税率': tax_rate,
                '金額': total_amount
            }])
    
            st.session_state.df = pd.concat([st.session_state.df, new_data], ignore_index=True)

            st.rerun()
    else:
        from_acc = st.selectbox("出金元", list(balances.keys()), key="from_acc")
        to_acc = st.selectbox("入金先", list(balances.keys()), key="to_acc")
        transfer_amount = st.sidebar.number_input("移動する金額", min_value=0, step=1)
    
        if st.button("振替を記録する", type = "primary"):
            if from_acc == to_acc:
                st.warning("出金元と入金先が同じです。")
            elif transfer_amount > 0:
                acc_label = f"{from_acc} → {to_acc}"
                new_data = pd.DataFrame([{
                    '日付': date,
                    '種別': type_,
                    'アカウント': acc_label,
                    '大分類': "-",
                    '詳細項目': "-",
                    '品目': "-",
                    '単価': transfer_amount,
                    '数量': 1,
                    '税区分': "-",
                    '税率': "-",
                    '金額': transfer_amount
                }])
                st.session_state.df = pd.concat([st.session_state.df, new_data], ignore_index=True)
                st.sidebar.success("資金の移動を記録しました。")
            else:
                st.sidebar.warning("1円以上の金額を入力してください。")

# ==========================================
# 11. タブ1：支出の分析の描画

# step9で設定したタブ1：支出の分析の描画を行っています。
# 日付ごと、月ごとに分けて集計をするセクション、その月、その日の内訳を示すセクションがあります。また、それぞれのデータをcsvとしてダウンロードできるようにしております。

# ==========================================

with tab1:
    st.markdown("### 支出の分析")

    if not st.session_state.df.empty:
        expense_data = st.session_state.df[st.session_state.df['種別']=='支出'].copy()

        expense_data['金額'] = pd.to_numeric(expense_data['金額'].astype(str).str.replace(',',''),errors='coerce')

        if not expense_data.empty:
            expense_data['日付_dt']=pd.to_datetime(expense_data['日付'],errors='coerce')
            expense_data['年月']=expense_data['日付_dt'].dt.strftime('%Y/%m')

            view_mode = st.radio("集計単位を選択", ["月別","日別"],horizontal=True)
            time_col = '年月' if view_mode == '月別' else '日付'

            st.markdown(f"** {view_mode}の支出推移 **")
            trend_data = expense_data.groupby(time_col)['金額'].sum()
            st.bar_chart(trend_data)

            st.markdown(f"** {view_mode} × 項目別の集計表 **")
            pivot_df = expense_data.pivot_table(index = time_col, columns='大分類', values = '金額', aggfunc = 'sum', fill_value = 0)
            pivot_df['合計'] = pivot_df.sum(axis=1)
            pivot_df = pivot_df.sort_index(ascending = False)

            st.dataframe(pivot_df, width ='stretch')

            csv_summary = pivot_df.to_csv().encode('utf-8-sig')
            st.download_button(
                label=f"{view_mode}の集計表をCSVでダウンロード",
                data=csv_summary,
                file_name = f"expense_summry_{view_mode}.csv",
                mime = 'text/csv',
                type = "primary"
            )

            st.markdown("---")

            st.markdown(f"**特定の期間の割合**")
            periods = pivot_df.index.tolist()
            selected_period = st.selectbox(f"内訳を見たい{view_mode[:-1]}を選択してください", periods)

            period_data = expense_data[expense_data[time_col]==selected_period]
            period_summary = period_data.groupby('大分類')['金額'].sum().reset_index()

            total_for_period = period_summary['金額'].sum()
            period_summary['割合(%)']= (period_summary['金額']/total_for_period * 100).round(1)
            period_summary = period_summary.sort_values('金額', ascending = False)

            col_a, col_b = st.columns(2)
            with col_a:
                st.metric(f"【{selected_period}】の支出合計", f"￥{int(total_for_period):,}")
                st.dataframe(period_summary.set_index('大分類'), width = 'stretch')

            with col_b:
                st.write("項目ごとの割合")
                st.bar_chart(period_summary.set_index('大分類')['金額'])
        else:
            st.info("支出データがありません")

    else:
        st.info("データがありません")  

# ==========================================
# 12. タブ2：履歴の一覧の描画

# step9で設定したタブ2：履歴の一覧の描画を行っています。
# 種別、大分類、詳細項目のそれぞれをフィルターし、見たい部分のみを見れるようにしております。また、csvとしてダウンロードできるようにしております。

# ==========================================

with tab2:
    st.subheader('データの一覧')

    if not st.session_state.df.empty:
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            filter_type = st.selectbox("種別", ["すべて", "支出", "収入", "振替"])
        with col_f2:
            major_opt = ["すべて"] + st.session_state.df['大分類'].dropna().unique().tolist()
            filter_major = st.selectbox("大分類", major_opt)
        with col_f3:
            detail_opt = ["すべて"]+ st.session_state.df['詳細項目'].dropna().unique().tolist()
            filter_detail = st.selectbox("詳細項目", detail_opt)

        filtered_df = st.session_state.df.copy()

        if filter_type != "すべて":
            filtered_df = filtered_df[filtered_df["種別"]==filter_type]
        if filter_major != "すべて":
            filtered_df = filtered_df[filtered_df["大分類"]==filter_type]
        if filter_detail != "すべて":
            filtered_df = filtered_df[filtered_df["詳細項目"]==filter_type]

        filtered_df['日付']=pd.to_datetime(filtered_df['日付'])

        display_filtered_df = filtered_df.sort_values(by="日付", ascending= False)

        st.write(f"表示中のデータ：**{len(display_filtered_df)}件**")
        st.dataframe(display_filtered_df, width = "stretch", hide_index = True)

        st.markdown("---")
        st.write("現在表示されている詳細データをCSV形式でダウンロードします。")
        csv_data = display_filtered_df.to_csv().encode('utf-8-sig')
        st.download_button(
                label=f"履歴をCSVでダウンロード",
                data=csv_data,
                file_name = f"expense_data_{datetime.now().strftime('%Y%m%d')}.csv",
                mime = 'text/csv',
                type = "primary"
            )
    else:
        st.info("履歴がありません")

# ==========================================
# 13. タブ3：設定・データ管理の描画

# step9で設定したタブ3：設定・データ管理の描画を行っています。
# 以下のセクションがあります。
# ・既存アカウントの初期残高を変更するセクション
# ・新規アカウントを追加するセクション
# ・既存のアカウント名を変更するセクション
# ・履歴を編集するセクション
# ・過去の履歴を削除するセクション

# ==========================================

with tab3:
    st.markdown("### データ管理")

    st.subheader("アカウント(口座・カード)の管理")

    with st.form("account_management_form"):
        st.markdown("既存アカウントの初期残高を変更")
        new_bals = {}
        acc_list_keys = list(st.session_state.accounts_init.keys())

        for i in range(0, len(acc_list_keys),2):
            col_a1, col_a2 = st.columns(2)
            acc1 = acc_list_keys[i]
            new_bals[acc1]=col_a1.number_input(f"【{acc1}】", value = st.session_state.accounts_init[acc1], step=1)
            if i+1 < len(acc_list_keys):
                acc2 = acc_list_keys[i+1]
                new_bals[acc2]=col_a2.number_input(f"【{acc2}】", value = st.session_state.accounts_init[acc2], step=1)

        st.markdown("---")
        st.markdown("新規アカウントの追加")
        new_acc_name = st.text_input("追加する名前(例：PayPay, 三井住友カード)")
        new_acc_bal = st.number_input("初期残高（初期値は0。未払い残高はマイナスで表記)", value = 0, step = 1)

        if st.form_submit_button("残高の更新・アカウントの追加"):
            for acc, b in new_bals.items():
                st.session_state.accounts_init[acc] = b
            if new_acc_name != "":
                st.session_state.accounts_init[new_acc_name] = new_acc_bal
            
            st.success("アカウント情報を更新しました")
            st.rerun()
        
    with st.form("account_rename_form"):
        st.markdown("既存のアカウント名を変更")
        old_acc_name = st.selectbox("名前を変更するアカウント", acc_list_keys)
        new_acc_name_edit = st.text_input("新しい名前","")

        if st.form_submit_button("アカウント名を変更"):
            if new_acc_name_edit and new_acc_name_edit != old_acc_name:
                val = st.session_state.accounts_init.pop(old_acc_name)
                st.session_state.accounts_init[new_acc_name_edit]=val

                def replace_acc_name(x):
                    x_str = str(x)
                    if x_str == old_acc_name:
                        return new_acc_name_edit
                    elif "→" in x_str:
                        return x_str.replace(old_acc_name, new_acc_name_edit)
                    return x_str
                
                st.session_state.df['アカウント']=st.session_state.df['アカウント'].apply(replace_acc_name)

                st.success(f"「{old_acc_name}」を「{new_acc_name_edit}」に変更しました")
                st.rerun()
            elif new_acc_name_edit == old_acc_name:
                st.warning("名前が変わっていません")
            else:
                st.warning("名前を入力してください")

    st.markdown("---")

    st.subheader("**履歴の編集**")

    if not st.session_state.df.empty:
        edit_options = []
        for i, row in st.session_state.df.iterrows():
            edit_options.append(f"[ID:{i}]{row['日付']}-{row['品目']}(￥{row['金額']})")
        
        edit_target = st.selectbox("編集する履歴を選択", edit_options)
        target_idx = int(edit_target.split("]")[0].replace("[ID:",""))
        current_data = st.session_state.df.loc[target_idx]

        with st.form("edit_form"):
            e_date = st.text_input("日付(YYYY/MM/DD)", value=current_data['日付'])

            if current_data['種別'] == '振替':
                all_accs = st.session_state.df['アカウント'].dropna().unique().tolist()
                valid_accs = [acc for acc in all_accs if " → " not in acc]
                current_acc_str = str(current_data['アカウント'])
                if " → " in current_data:
                    curr_f, curr_t = current_acc_str.split(" → ")
                else:
                    curr_f, curr_t = valid_accs[0], valid_accs[1]
                if curr_f not in valid_accs:
                    valid_accs.insert(0,curr_f)
                if curr_t not in valid_accs:
                    valid_accs.insert(0, curr_t)

                e_acc_f = st.selectbox("出金元", valid_accs, index=valid_accs.index(curr_f))
                e_acc_t = st.selectbox("入金先", valid_accs, index=valid_accs.index(curr_t))
                if e_acc_f != e_acc_t:
                    e_acc = f"{e_acc_f} → {e_acc_t}"
                else:
                    st.warning("出金元と入金先が同じです。異なるアカウントにしてください。")
                    e_acc = current_acc_str
            else:
                acc_opts = list(st.session_state.accounts_init.keys())
                if current_data['アカウント'] not in acc_opts:
                    acc_opts.insert(0,str(current_data['アカウント']))
                e_acc = st.selectbox("アカウント", acc_opts, index=acc_opts.index(str(current_data['アカウント'])))

            e_major = st.text_input("大分類", value = current_data['大分類'])
            e_detail = st.text_input("詳細項目", value = current_data['詳細項目'])
            e_item = st.text_input("品目", value = current_data['品目'])
            e_amt = st.number_input("金額", value = int(str(current_data['金額']).replace(",","")), step = 1)

            if st.form_submit_button("この内容で上書き"):
                st.session_state.df.loc[target_idx, '日付']=str(e_date)
                st.session_state.df.loc[target_idx, 'アカウント']=str(e_acc)
                st.session_state.df.loc[target_idx, '大分類']=str(e_major)
                st.session_state.df.loc[target_idx, '詳細項目']=str(e_detail)
                st.session_state.df.loc[target_idx, '品目']=str(e_item)
                st.session_state.df.loc[target_idx, '金額']=str(e_amt)

                st.succes("履歴を更新しました")
                st.rerun()
    else:
        st.info("編集できる履歴がありません")

    st.markdown("---")

    st.subheader("過去の履歴を削除")
    if not st.session_state.df.empty:
        delete_target = st.selectbox("削除するデータを選択", edit_options)
        if st.button("この履歴を削除", type = "primary"):
            del_idx = int(delete_target.split("]")[0].replace("[ID:",""))
            st.session_state.df = st.session_state.df.drop(del_idx).reset_index(drop=True)
            st.success("履歴を削除しました")
            st.rerun()
