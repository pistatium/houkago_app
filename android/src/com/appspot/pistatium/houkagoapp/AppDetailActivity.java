package com.appspot.pistatium.houkagoapp;

import java.util.List;

import org.androidannotations.annotations.AfterViews;
import org.androidannotations.annotations.Click;
import org.androidannotations.annotations.EActivity;
import org.androidannotations.annotations.ViewById;

import android.content.Intent;
import android.content.res.Resources;
import android.net.Uri;
import android.os.Bundle;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;
import android.widget.Toast;
import 	android.text.TextUtils;
import com.android.volley.RequestQueue;
import com.android.volley.VolleyError;
import com.android.volley.Request.Method;
import com.android.volley.Response.ErrorListener;
import com.android.volley.Response.Listener;
import com.android.volley.toolbox.ImageLoader;
import com.android.volley.toolbox.NetworkImageView;
import com.android.volley.toolbox.Volley;
import com.appspot.pistatium.houkagoapp.R.id;
import com.appspot.pistatium.houkagoapp.base.FragmentActivityBase;
import com.appspot.pistatium.houkagoapp.libs.AppImageCache;
import com.appspot.pistatium.houkagoapp.libs.AppListRequest;
import com.appspot.pistatium.houkagoapp.libs.DetailRequest;
import com.appspot.pistatium.houkagoapp.models.AppModel;
import com.appspot.pistatium.houkagoapp.models.DeveloperModel;
import com.appspot.pistatium.utilities.L;
import com.appspot.pistatium.utilities.Utils;

@EActivity(R.layout.activity_detail)
public class AppDetailActivity extends FragmentActivityBase{
	@ViewById Button go_market_btn;
	@ViewById TextView app_title;
	@ViewById TextView profile_text;
	@ViewById TextView developer_name;
	@ViewById ScrollView scroll_view;
	@ViewById NetworkImageView app_icon;
	@ViewById NetworkImageView profile_image;
	@ViewById LinearLayout inner_detail;
	@ViewById LinearLayout profile_layout;
	
	AppModel app;
	private RequestQueue mQueue;
	
	@AfterViews
	void initLayout(){
		initDrawer();
	}
	
	@AfterViews
	void initItems(){
		Intent i = getIntent();
		long app_id = i.getLongExtra("app_id", 0);
		app = AppModel.getById(app_id);
		if (app == null) {
			Toast.makeText(getApplicationContext(), "このアプリはありません", Toast.LENGTH_SHORT).show();
			finish();
		}
		
		mQueue = Volley.newRequestQueue(getApplicationContext());

		getDeveloper(app.getDeveloper_id());
		
		app_icon.setImageUrl(app.getApp_image(), new ImageLoader(mQueue, new AppImageCache()));	
		app_title.setText(app.getApp_name());
		scroll_view.setFadingEdgeLength(6);
		addContent("アプリの詳細", app.getPr_summary());
		addContent("作ったきっかけ",app.getWhy_create());
		addContent("開発時のこだわり",app.getProduct_point());
		addContent("こんな人に使って欲しい",app.getTarget_user());	
	}
	
	void getDeveloper(long developer_id){
		DeveloperModel developer = DeveloperModel.getById(developer_id);
		if (developer != null) {
			setProfileLayout(developer);
		}
		
		String url = "http://houkago-no.appspot.com/api/app/detail/"
				+ app.getApp_id()
				+ "?client=" + "kimihiro_n_5631943370604544"
				+ "&key="   + "689f9b4bef67d6027ff954dad24a046189e896bc"
				+ "&version=1&count=20";
			L.d(url);
			mQueue.add(new DetailRequest(Method.GET, url,
					new Listener<DeveloperModel>() {
		                @Override
		                public void onResponse(DeveloperModel developer) {
		                	setProfileLayout(developer);
		                }
		            }, new ErrorListener() {
						@Override
						public void onErrorResponse(VolleyError error) {	
						}
		            }
		    ));
		    mQueue.start();
	}
	
	@Click(R.id.go_market_btn)
	void onClickGoMarket(){
		Uri uri = Uri.parse("market://details?id=" + app.getPackage_name());
		Intent i = new Intent(Intent.ACTION_VIEW,uri);
		startActivity(i);
	}
	
	private void addContent(String title, String content) {
		if (!TextUtils.isEmpty(content)) {
			Resources res = getResources();
			TextView tv_title = new TextView(getApplicationContext());
			tv_title.setText(title);
			tv_title.setTextSize(20.0f);
			tv_title.setTextColor(res.getColor(R.color.primary));
			TextView tv_content = new TextView(getApplicationContext());
			tv_content.setText(content);
			tv_content.setTextSize(14.0f);
			tv_content.setTextColor(res.getColor(R.color.base_text));
			tv_content.setPadding(30, 5, 0, 30);
			inner_detail.addView(tv_title);
			inner_detail.addView(tv_content);
		}
	}
	private void setProfileLayout(DeveloperModel developer){
		String developer_image = "http://houkago-no.appspot.com/uploaduser/icon/" + developer.getDeveloper_id();
		profile_image.setImageUrl(developer_image, new ImageLoader(mQueue, new AppImageCache()));
		developer_name.setText(developer.getUser_name());
		profile_text.setText(developer.getProfile());
		profile_layout.setVisibility(View.VISIBLE);
		
		if (TextUtils.isEmpty(developer.getSite_addr())) {
			return;
		}
		Uri uri = Uri.parse(developer.getSite_addr());
		profile_layout.setOnClickListener(Utils.openUri(this, uri));
		
	}
	
}
