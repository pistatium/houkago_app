package com.appspot.pistatium.houkagoapp;

import java.util.List;

import javax.xml.transform.TransformerException;

import org.androidannotations.annotations.EActivity;
import org.androidannotations.annotations.rest.Rest;

import com.activeandroid.content.ContentProvider;
import com.android.volley.Request.Method;
import com.android.volley.RequestQueue;
import com.android.volley.Response.ErrorListener;
import com.android.volley.Response.Listener;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.Volley;
import com.appspot.pistatium.houkagoapp.base.FragmentActivityBase;
import com.appspot.pistatium.houkagoapp.libs.AppCursorAdapter;
import com.appspot.pistatium.houkagoapp.libs.AppListRequest;

import com.appspot.pistatium.houkagoapp.models.AppModel;
import com.appspot.pistatium.utilities.L;

import android.net.Uri;
import android.os.Bundle;
import android.app.Activity;
import android.app.Dialog;
import android.content.Intent;
import android.database.Cursor;
import android.graphics.Bitmap;
import android.support.v4.app.ActionBarDrawerToggle;
import android.support.v4.app.Fragment;
import android.support.v4.app.LoaderManager;
import android.support.v4.content.CursorLoader;
import android.support.v4.content.Loader;
import android.support.v4.widget.DrawerLayout;
import android.support.v7.app.ActionBar;
import android.view.KeyEvent;
import android.view.Menu;
import android.view.Window;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.ListView;
import android.widget.Toast;

@EActivity
public class MainActivity extends FragmentActivityBase implements
LoaderManager.LoaderCallbacks<Cursor> {

	
	private RequestQueue mQueue;
	private AppCursorAdapter adapter;
	ListView listView;
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		//requestWindowFeature(Window.FEATURE_NO_TITLE);
		
		setContentView(R.layout.activity_main);
		adapter = new AppCursorAdapter(this, null, 0);
		this.getSupportLoaderManager().initLoader(0, null,this);
		listView = (ListView) findViewById(R.id.item_list_view);
		listView.setAdapter(adapter);
		//webview = (WebView) findViewById(R.id.main_web_view);
		mQueue = Volley.newRequestQueue(getApplicationContext());
	    requestApps();
	    initDrawer();
	}


	private void requestApps(){
		String url = "http://houkago-no.appspot.com/api/app/recent/Android?"
			+ "client=" + "kimihiro_n_5631943370604544"
			+ "&key="   + "689f9b4bef67d6027ff954dad24a046189e896bc"
			+ "&version=1&count=20";
		L.d(url);
		mQueue.add(new AppListRequest(Method.GET, url,
				new Listener<List<AppModel>>() {
	                @Override
	                public void onResponse(List<AppModel> apps) {
	                	
	                }
	            }, new ErrorListener() {

					@Override
					public void onErrorResponse(VolleyError error) {
						// TODO Auto-generated method stub
						
					}


	            }
	    ));
	    mQueue.start();

	}
	
	@Override
	protected void onDestroy() {
		// TODO Auto-generated method stub
		super.onDestroy();
		getSupportLoaderManager().destroyLoader(0);
	}
	// LoaderManager縲�-------------------------------

	@Override
	public Loader<Cursor> onCreateLoader(int id, Bundle bundle) {
		return new CursorLoader(this, ContentProvider.createUri(
				AppModel.class, null), null, null, null, "created_stamp desc");
	}

	@Override
	public void onLoadFinished(Loader<Cursor> loader, Cursor cursor) {
		// TODO Auto-generated method stub
		
		L.d("cursor count: " + cursor.getCount());
		adapter.swapCursor(cursor);
		//adapter.notifyDataSetChanged();
	}

	@Override
	public void onLoaderReset(Loader<Cursor> loader) {
		// TODO Auto-generated method stub
		adapter.swapCursor(null);
	}
	
}
