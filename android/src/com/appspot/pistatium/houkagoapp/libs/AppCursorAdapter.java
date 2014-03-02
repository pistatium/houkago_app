package com.appspot.pistatium.houkagoapp.libs;


import com.android.volley.RequestQueue;
import com.android.volley.toolbox.ImageLoader;
import com.android.volley.toolbox.NetworkImageView;
import com.android.volley.toolbox.Volley;
import com.appspot.pistatium.houkagoapp.AppDetailActivity;
import com.appspot.pistatium.houkagoapp.AppDetailActivity_;
import com.appspot.pistatium.houkagoapp.R;
import com.appspot.pistatium.houkagoapp.models.AppModel;
import com.appspot.pistatium.utilities.L;

import android.content.Context;
import android.content.Intent;
import android.database.Cursor;
import android.support.v4.widget.CursorAdapter;
import android.view.LayoutInflater;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;

public class AppCursorAdapter  extends CursorAdapter implements OnClickListener{
	private static final int APP_ID = R.id.app;
	
	static class ViewHolder {  
		TextView app_title;
		TextView app_tagline;
		NetworkImageView app_icon;
	}

	private LayoutInflater inflater;
	RequestQueue queue;
	Context app_context;
	public AppCursorAdapter(Context context, Cursor c, int flags) {
		super(context, c, flags);
		//this.context = context;
		queue = Volley.newRequestQueue(context);
		app_context = context;
		this.inflater = (LayoutInflater)context.getSystemService(context.LAYOUT_INFLATER_SERVICE);
	}

	@Override
	public void bindView(View view, Context context, Cursor c) {
		// TODO Auto-generated method stub
		L.d("binded");
		AppModel app = new AppModel();
	    app.loadFromCursor(c);
	    //View view = convertView;
		ViewHolder holder; 
		holder = (ViewHolder)view.getTag(R.layout.app_cell);
		holder.app_title.setText(app.getApp_name());
		holder.app_tagline.setText(app.getTagline());
		holder.app_icon.setImageUrl(app.getApp_image(), new ImageLoader(queue, new AppImageCache()));
		if (app.is_read()) {
			holder.app_title.setTextColor(context.getResources().getColor(R.color.primary_light));
		} else {
			holder.app_title.setTextColor(context.getResources().getColor(R.color.primary));
		}
		view.setTag(APP_ID, app);
		view.setOnClickListener(this);
	}

	@Override
	public View newView(Context context, Cursor cursor, ViewGroup viewGroup) {
		View view = this.inflater.inflate(R.layout.app_cell, null);
		
		ViewHolder holder;  
		holder = new ViewHolder();
		
		holder.app_title = (TextView)view.findViewById(R.id.app_title);
		holder.app_tagline = (TextView)view.findViewById(R.id.app_tagline);
		holder.app_icon = (NetworkImageView)view.findViewById(R.id.app_icon);
		view.setTag(R.layout.app_cell, holder);
		return view;
	}

	@Override
	public void onClick(View v) {
		AppModel app = (AppModel)v.getTag(R.id.app);
		app.set_read(true);
		app.save();
		L.d("id" + app.getApp_id());
		Intent i = new Intent(app_context,AppDetailActivity_.class);
		i.putExtra("app_id", app.getApp_id());
		app_context.startActivity(i);
	}

}
