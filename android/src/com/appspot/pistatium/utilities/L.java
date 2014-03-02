package com.appspot.pistatium.utilities;
/**
* = Customized Log Class =
*   ログを使いやすくラップしたもの
* == 使い方 ==
* 	L.d("fuga","fuga");
*	L.d(this,"hoge");
*	L.d("piyo");
*/



import com.appspot.pistatium.houkagoapp.BuildConfig;

import android.content.Context;
import android.util.Log;

/*
 * Custmized Log Class
 */
public class L {
	
	// 共通タグ
	static String TAG_LABEL = "pista ";
	// 本番apkの場合、初回のみメッセージを出す
	static boolean FirstFlag = true;
	
	/*
	 * デバッグ署名の時のみログ表示
	 */
	static public void d(String tag, String msg, Throwable tr){
		tag = TAG_LABEL + tag;
		//IS_DEBUG == false でもデバッグAPKの時はログを出す
		if (BuildConfig.DEBUG == false){
			if (FirstFlag) {
				Log.d(TAG_LABEL, "== This is production apk ==");
				FirstFlag = false;
			}
			return;
		}
		if(tr == null){
			Log.d(tag, msg);
		} else {
			Log.d(tag,msg,tr);
		}
	}
	
	/*
	 * 標準バージョン
	 */
	static public void d(String tag, String msg){
		L.d(tag, msg, null);
	}

	/*
	 * タグ不要バージョン
	 */
	static public void d(String msg){
		L.d("", msg, null);
	}
	
	/*
	 * コンテキストを渡すとアクティビティ名をタグに追加
	 */
	static public void d(Context context, String msg){
		String tag = context.getClass().getSimpleName();
		L.d(tag, msg, null);
	}
	
	/*
	 * オブジェクト対応バージョン(テスト)
	 */
	static public void d(Context context, Object o) {
		if(o != null){
			L.d(context, o.toString() + " (" +o.getClass() + ")" );
		} else {
			L.d(context, "Value is NULL!");			
		}
	}
	
}
