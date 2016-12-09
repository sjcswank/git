package org.launchcode.blogz.controllers;

import java.util.List;

import org.launchcode.blogz.models.User;
import org.launchcode.blogz.models.dao.PostDao;
import org.launchcode.blogz.models.dao.UserDao;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
public class BlogController extends AbstractController {
	
	@Autowired
	UserDao UserDao;
	
	@Autowired
	PostDao PostDao;

	@RequestMapping(value = "/")
	public String index(Model model){
		
		//get all unique users from db
		List<User> users = UserDao.findAll();
		
		//pass to index.html
		model.addAttribute("users", users);
		
		return "index";
	}
	
	@RequestMapping(value = "/blog")
	public String blogIndex(Model model) {
		
		model.addAttribute("posts", PostDao.findAll());
		
		return "blog";
	}
	
}
