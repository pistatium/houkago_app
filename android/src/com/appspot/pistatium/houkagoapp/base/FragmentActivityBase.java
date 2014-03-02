package com.appspot.pistatium.houkagoapp.base;

import com.appspot.pistatium.houkagoapp.R;
import com.appspot.pistatium.utilities.Utils;
import com.google.analytics.tracking.android.EasyTracker;

import android.annotation.SuppressLint;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.support.v4.app.ActionBarDrawerToggle;
import android.support.v4.app.FragmentActivity;
import android.support.v4.widget.DrawerLayout;
import android.support.v7.app.ActionBar;
import android.support.v7.app.ActionBarActivity;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.Window;

@SuppressLint("NewApi")
public class FragmentActivityBase extends ActionBarActivity {
	protected ActionBarDrawerToggle mDrawerToggle;
	protected DrawerLayout mDrawer;

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		ActionBar ab = getSupportActionBar();
		ab.setDisplayHomeAsUpEnabled(true);
		ab.setHomeButtonEnabled(true);
	}

	protected void initDrawer() {
		mDrawer = (DrawerLayout) findViewById(R.id.drawer_layout);
		if (mDrawer == null) {
			return;
		}
		mDrawerToggle = new ActionBarDrawerToggle(this, mDrawer,
				R.drawable.ic_l_white96, R.string.hello_world,
				R.string.hello_world) {
		};
		mDrawer.setDrawerListener(mDrawerToggle);
		mDrawer.findViewById(R.id.btn_about_circle).setOnClickListener(new OnClickListener() {
					@Override
					public void onClick(View v) {
						Uri uri = Uri
								.parse("http://houkago-no.appspot.com/about");
						Intent i = new Intent(Intent.ACTION_VIEW, uri);
						startActivity(i);
					}
				});
		
		Uri uri = Uri.parse("http://houkago-no.appspot.com/regist");
		mDrawer.findViewById(R.id.btn_enter_circle).setOnClickListener(
				Utils.openUri(this, uri));
		
		mDrawer.findViewById(R.id.share_button).setOnClickListener(new OnClickListener() {
					@Override
					public void onClick(View v) {
						Intent i = new Intent(Intent.ACTION_SEND);
						i.putExtra(Intent.EXTRA_TEXT,
								getString(R.string.share_app));
						i.setType("text/plain");
						startActivity(i);
					}
				});
		mDrawer.findViewById(R.id.evaluate_button).setOnClickListener(new OnClickListener() {
					@Override
					public void onClick(View v) {
						Uri uri = Uri.parse(getString(R.string.gp_link));
						Intent i = new Intent(Intent.ACTION_VIEW, uri);
						startActivity(i);
					}
				});
		ActionBar ab = getSupportActionBar();
		ab.setDisplayHomeAsUpEnabled(true);
		ab.setHomeButtonEnabled(true);
		ab.setDisplayUseLogoEnabled(true);

	}

	@Override
	public void onStart() {
		super.onStart();
		EasyTracker.getInstance().activityStart(this); // Add this method.
	}

	@Override
	public void onStop() {
		super.onStop();
		EasyTracker.getInstance().activityStop(this); // Add this method.
	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		// getMenuInflater().inflate(R.menu.main, menu);
		return true;
	}

	@Override
	public boolean onOptionsItemSelected(MenuItem item) {
		if (mDrawerToggle != null && mDrawerToggle.onOptionsItemSelected(item)) {
			return true;
		}
		return super.onOptionsItemSelected(item);
	}

}
