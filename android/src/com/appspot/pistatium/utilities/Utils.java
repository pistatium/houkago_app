package com.appspot.pistatium.utilities;

import android.annotation.TargetApi;
import android.content.Context;
import android.content.Intent;
import android.net.Uri;
import android.os.Build;
import android.view.View;
import android.view.View.OnClickListener;

public class Utils {


	@TargetApi(Build.VERSION_CODES.HONEYCOMB)
	static public void setAlpha(View v, float alpha) {
		if (Build.VERSION.SDK_INT >= 11) {
			v.setAlpha(alpha);
		} else {
			if (alpha < 1.0f) {
				v.setVisibility(View.INVISIBLE);
			} else {
				v.setVisibility(View.VISIBLE);
			}
		}
	}
	static public int getPx(Context appContext, int dimensionDp) {
	    float density = appContext.getResources().getDisplayMetrics().density;
	    return (int) (dimensionDp * density + 0.5f);
	}
	
	static public OnClickListener openUri(final Context context, final Uri uri){
		return new OnClickListener() {
			@Override
			public void onClick(View v) {
				Intent i = new Intent(Intent.ACTION_VIEW, uri);
				context.startActivity(i);
				
			}
		};
	}
}
