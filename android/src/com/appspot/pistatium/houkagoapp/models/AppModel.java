package com.appspot.pistatium.houkagoapp.models;

import java.sql.Date;
import java.util.List;

import lombok.Data;
import lombok.Getter;
import lombok.Setter;

import net.vvakame.util.jsonpullparser.annotation.JsonKey;
import net.vvakame.util.jsonpullparser.annotation.JsonModel;

import android.provider.BaseColumns;

import com.activeandroid.Model;
import com.activeandroid.annotation.Column;
import com.activeandroid.annotation.Table;
import com.activeandroid.query.Select;
import com.appspot.pistatium.utilities.L;

@Data
@JsonModel(decamelize = false)
@Table(name = "App", id = BaseColumns._ID)
public class AppModel extends Model {

	public AppModel() {
		L.d("create");
	}
	
	@Column(name = "created_at")
	Date created_at = new Date(System.currentTimeMillis());
	
	@JsonKey
	@Column(name = "created_stamp")
	long created_stamp = 0;

	
	@Column(name = "updated_at")
	Date updated_at = new Date(System.currentTimeMillis());

	@JsonKey
	@Column(name = "updated_stamp")
	long updated_stamp = 0;
	
	@JsonKey(value = "id")
	@Column(name = "app_id", unique = true, onUniqueConflict = Column.ConflictAction.REPLACE)
	long app_id;

	@JsonKey
	@Column(name = "status")
	int status;

	@JsonKey
	@Column(name = "app_name")
	String app_name = "";

	@JsonKey
	@Column(name = "developer_id")
	long developer_id;

	@JsonKey
	@Column(name = "dl_link")
	String dl_link;

	@JsonKey
	@Column(name = "package_name")
	String package_name;

	@JsonKey
	@Column(name = "tagline")
	String tagline;

	@JsonKey
	@Column(name = "pr_summary")
	String pr_summary;

	@JsonKey
	@Column(name = "why_create")
	String why_create;

	@JsonKey
	@Column(name = "target_user")
	String target_user;

	@JsonKey
	@Column(name = "product_point")
	String product_point;

	@JsonKey
	@Column(name = "thumbnail")
	String thumbnail;

	@JsonKey
	@Column(name = "app_icon")
	String app_image;
	
	@JsonKey
	@Column(name = "category")
	String category;

	@JsonKey
	@Column(name = "creator_push")
	int creator_push;

	@Column(name = "is_fav")
	boolean is_fav = false;

	@Column(name = "is_read")
	boolean is_read = false;

	
	public AppModel update(AppModel app){
		if (this.updated_stamp == app.updated_stamp) {
			//return this;
		}
		this.app_name = app.app_name;
		this.category = app.category;
		this.creator_push = app.creator_push;
		this.dl_link = app.dl_link;
		this.package_name = app.package_name;
		this.pr_summary = app.pr_summary;
		this.product_point = app.product_point;
		this.status = app.status;
		this.tagline = app.tagline;
		this.target_user = app.target_user;
		this.thumbnail = app.thumbnail;
		this.updated_stamp = app.updated_stamp;
		this.why_create =app.why_create;
		this.updated_at = new Date(System.currentTimeMillis());
		this.save();
		return this;
	}
	
	public static List<AppModel> getLatest(int count) {
		List<AppModel> apps = new Select().from(AppModel.class).orderBy("created_stamp desc").limit(count).execute();
		return apps;
	}
	
	public static AppModel getLatestOne(){
		List<AppModel> apps = getLatest(1);
		if (apps != null && apps.size() > 0) {
			return apps.get(0);
		}
		return null;
	}
	
	public static AppModel getById(long app_id){
		return new Select().from(AppModel.class)
				.where("app_id = ?", app_id).executeSingle();
	}
}
