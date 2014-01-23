package com.myfeetr.feetr.model;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;

import com.activeandroid.Model;
import com.activeandroid.annotation.Column;
import com.activeandroid.annotation.Table;
import com.activeandroid.query.Select;
import com.myfeetr.feetr.util.Utils;

@Table(name="MyFeed")
public class MyFeedModel extends Model {

	@Column(name="title")
	public String title = "";

	@Column(name="status")
	public int status = 1; // 1:valid  0:removed

	@Column(name="position")
	public int position = 0; // 画面の何番目のフラグメントが割り当てられているか

	@Column(name = "created_at")
	public Date created_at = new Date();

	@Column(name = "updated_at")
	public Date updated_at = new Date();
	
	static final long NOT_FOUND = -1;
	
	/* 含むフィルタのfor文の管理 */
	static final int INCLUDE_START = 1000;
	static final int INCLUDE_DOING = 1010;
	static final int INCLUDE_END = 1100;


	static public List<ItemModel> getRecentItems(int limit, int offset, long my_feed_position){

		MyFeedModel myfeed = new Select().from(MyFeedModel.class)
				.where("status = 1")
				.orderBy("Id")
				.limit(1).offset((int)my_feed_position).executeSingle();

		if (myfeed == null){
			return new ArrayList<ItemModel>();
		}

		return new Select().from(ItemModel.class)
				.where("my_feed_id = ?",  myfeed.getId())
				.orderBy("pub_date DESC")
				.limit(limit).offset(offset).execute();
	}

	/* Itemをフィルターにかけ、その結果を取得 */
	static public List<ItemModel> getFilteredItems(int limit, int offset, long my_feed_id){

		FilterModel filterModel = FilterModel.getByFeedId(my_feed_id);

		if (filterModel == null) {
			filterModel = new FilterModel();
			filterModel.include_word = "";
			filterModel.remove_word = "";
			filterModel.tw_num = 0;
			filterModel.hour_num = 0;
		}

		/* フィルター文字の配列 */
		String includeWords[] = Utils.filterParse(filterModel.include_word);
		String removeWords[] = Utils.filterParse(filterModel.remove_word);

		int rtCount = filterModel.tw_num;
		int hourCount = filterModel.hour_num;

		StringBuilder query = new StringBuilder();

		/* ？を使ったSQL文に利用
		StringBuilder keyWord = new StringBuilder();
		if (!"".equals(includeWords[0])) {
			for(int i=0;i<includeWords.length;i++){
				L.d("sake filter word "+ includeWords[i]);
				keyWord.append(" , %%"+includeWords[i]+"%%");
				query.append(" and description like ?");
			}
		}
		if (!"".equals(removeWords[0])) {
			for(int i=0;i<removeWords.length;i++){
				L.d("sake filter word "+ removeWords[i]);
				keyWord.append(" , %%"+removeWords[i]+"%%");
				query.append(" and description not like ?");
			}
		}
		keyWord.toString();
		 */

		
		/*
		 * 含むフィルター。SQL文は、次のようになる
		 * and ((description like %target% or title like %target%) or (description like %target% or title like %target%) ...)
		 * この結果は、いくつかのtargetが、説明文かタイトルに含まれていれば、それらをすべて表示するという結果
		 * */
		int includeFlag = INCLUDE_START;
		/* 利用不可文字を設定した場合、空の配列がありえるので、continueで飛ばす */
		for(int i=0;i<includeWords.length;i++){
			if ("".equals(includeWords[i])) {
				continue;
			}
			
			/* 2週目以降、 「or」でつなぐ */
			if (includeFlag == INCLUDE_DOING) {
				query.append(" or ");
			}
			
			/* 1週目のみ、 頭に「and (」をつける */
			if (includeFlag == INCLUDE_START) {
				query.append("and (");
				includeFlag = INCLUDE_DOING;
			}
			query.append(" (description like \"%"+includeWords[i]+"%\" or title like \"%"+includeWords[i]+"%\")");
		}
		/* 最後のみ、 頭につけたものを閉じるために「)」をつける */
		if (includeFlag == INCLUDE_DOING) {
			query.append(")");
			includeFlag = INCLUDE_END;
		}

		/* 検索 */
//		query.append(" and (description like \"%"+includeWords[i]+"%\" or title like \"%"+includeWords[i]+"%\")");
		
		for(int i=0;i<removeWords.length;i++){
			if ("".equals(removeWords[i])) {
				continue;
			}
			query.append(" and description not like \"%"+removeWords[i]+"%\"");
		}
		for(int i=0;i<removeWords.length;i++){
			if ("".equals(removeWords[i])) {
				continue;
			}
			query.append(" and title not like \"%"+removeWords[i]+"%\"");
		}
		
		if (filterModel.tw_num != 0) {
			query.append(" and tw_num >= " + rtCount);
		}
		if (filterModel.hour_num != 0) {
			long minimamTime = Utils.filteredTime(hourCount);
			query.append(" and pub_date >= " + minimamTime);
		}

		List<ItemModel> list = new Select().from(ItemModel.class)
				.where("my_feed_id = ?" + query.toString() , my_feed_id)
				.orderBy("pub_date DESC")
				.limit(limit).offset(offset).execute();
		return list;
	}

	static public MyFeedModel getByMyFeedId(long my_feed_id){

		return new Select().from(MyFeedModel.class)
				.where("Id = ? and status = 1", my_feed_id)
				.executeSingle();
	}

	
	//MyFeedIdをポジションから取る
	static public long getMyFeedIdByPosition(int position){
		// jump pageをはさむので-1
		position--;
		if (isExist(position)){

			long my_feed_id =  new Select().from(MyFeedModel.class)
					.where("status=1")
					.offset(position)
					.limit(1)
					.executeSingle()
					.getId();
			return my_feed_id;

		}

		return NOT_FOUND;
	}


	static public long getMyFeedIdByCreated_at(int offset){
		long my_feed_id =  new Select().from(MyFeedModel.class)
				.where("status=1")
				.offset(offset)
				.limit(1)
				.orderBy("created_at DESC")
				.executeSingle()
				.getId();
		return my_feed_id;
	}

	/* 現在の画面にMyFeedModelが存在するのかを返す */
	static public boolean isExist(int position){
		MyFeedModel my_feed_model =  new Select().from(MyFeedModel.class)
				.where("status=1")
				.offset(position)
				.limit(1)
				.executeSingle();
		boolean isExist = true;
		if (my_feed_model == null) {
			isExist = false;
		}
		return isExist;
	}

	static public long getLastMyFeedId(){
		MyFeedModel my_feed_model =  new Select().from(MyFeedModel.class)
				.offset(0)
				.limit(1)
				.orderBy("Id DESC")
				.executeSingle();

		if (my_feed_model == null){
			return 0;
		}

		return my_feed_model.getId();
	}
	
	static public List<MyFeedModel>getMyFeeds(){
		return new Select().from(MyFeedModel.class)
				.where("status = 1")
				.orderBy("Id").execute();
	}

}