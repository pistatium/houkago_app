package com.appspot.pistatium.houkagoapp;

import org.json.JSONException;
import org.json.JSONObject;

import com.appspot.pistatium.utilities.L;

import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.Bundle;
import android.support.v4.app.NotificationCompat;
import android.widget.Toast;

/*

 {
 "channels": [ "" ],
 "type": "android",
 "data": {
 "action": "com.appspot.pistatium.houkagoapp.NEW_APP",
 "title": "Hello",
 "desc": "World"
 }
 }
 */
public class PushReciever extends BroadcastReceiver {
	Context context;

	public void onReceive(Context ctx, Intent intent) {
		try {
			// データを取得
			context = ctx;
			String action = intent.getAction();
			String channel = intent.getExtras().getString("com.parse.Channel");
			String data =  intent.getExtras().getString("com.parse.Data");
			L.d("receive:" + data);
			// jsonオブジェクトへパース
			JSONObject json = new JSONObject(data);

			String title = json.getString("title");
			String description = json.getString("desc");
			createNotice(title, description);
		} catch (JSONException e) {
			e.printStackTrace();
		}
	}

	private void createNotice(String title, String description) {
		Intent i = new Intent(context, SplashActivity.class);
		PendingIntent pi = PendingIntent.getActivity(context, 0, i, 0);

		// 120px
		Bitmap bmp = BitmapFactory.decodeResource(context.getResources(),
				R.drawable.ic_launcher120);
		NotificationCompat.Builder builder = new NotificationCompat.Builder(
				context);
		builder.setContentTitle(title);
		builder.setContentText(description);
		builder.setTicker(description);
		builder.setContentIntent(pi);
		builder.setLargeIcon(bmp);
		builder.setAutoCancel(true);
		builder.setSmallIcon(R.drawable.ic_launcher96);
		NotificationManager notificationManager = (NotificationManager) context
				.getSystemService(Context.NOTIFICATION_SERVICE);
		notificationManager.notify(0, builder.build());

	}
}